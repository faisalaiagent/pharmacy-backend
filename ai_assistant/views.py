import logging
from django.conf import settings
from groq import Groq
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.responses import success_response, error_response
from products.models import Product
from .models import AIConversation, AIMessage

logger = logging.getLogger(__name__)

MEDICAL_DISCLAIMER = (
    "\n\n---\n⚠️ **Medical Disclaimer:** This information is for educational purposes only and does not "
    "constitute medical advice. Always consult a licensed pharmacist or doctor before starting, "
    "stopping, or changing any medication. Do not self-diagnose or self-medicate."
)


class AIRateThrottle(UserRateThrottle):
    rate = "20/minute"
    scope = "ai_assistant"


def get_groq_client():
    return Groq(api_key=settings.GROQ_API_KEY)


def build_product_context(products):
    """Format product results into a concise text block for the AI system prompt."""
    if not products:
        return "No matching products found in our catalog."
    lines = []
    for p in products[:5]:
        line = f"- {p.name}"
        if p.generic_name:
            line += f" ({p.generic_name})"
        if p.strength:
            line += f" {p.strength}"
        line += f" | Price: {p.final_price} | Stock: {p.stock_status}"
        if p.requires_prescription:
            line += " | ⚕️ Requires Prescription"
        lines.append(line)
    return "\n".join(lines)


# ── 1. Medicine Search Assistant ─────────────────────────────────────────────

class MedicineSearchView(APIView):
    """
    Natural language medicine search. User types "medicine for headache" and
    gets matched products plus an AI explanation.
    """
    throttle_classes = [AIRateThrottle, AnonRateThrottle]
    permission_classes = [AllowAny]

    @extend_schema(tags=["AI Assistant"])
    def post(self, request):
        query = request.data.get("query", "").strip()
        if not query:
            return error_response("Query is required.")
        if len(query) > 500:
            return error_response("Query too long. Please keep it under 500 characters.")

        # Step 1: Search products matching the query terms
        matched_products = Product.objects.filter(
            is_active=True
        ).filter(
            name__icontains=query
        ) | Product.objects.filter(
            is_active=True, generic_name__icontains=query
        ) | Product.objects.filter(
            is_active=True, description__icontains=query
        )
        matched_products = matched_products.distinct().select_related("brand").prefetch_related("images")[:8]

        product_context = build_product_context(matched_products)

        # Step 2: Ask Groq to interpret the query and present results naturally
        system_prompt = f"""You are a helpful pharmacy assistant for an online pharmaceutical platform.
A customer is searching for medicine or health products.

Products available in our catalog matching their query:
{product_context}

Instructions:
- Suggest relevant products from the catalog above
- Briefly explain what each product is used for (1 sentence)
- Flag any that require a prescription
- Be helpful, clear, and professional
- Do NOT recommend specific dosages or substitute for medical advice
- Keep response under 200 words
"""
        try:
            client = get_groq_client()
            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ],
                max_tokens=400,
                temperature=0.3,
            )
            ai_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
        except Exception as e:
            logger.error("Groq API error (search): %s", str(e))
            return error_response("AI service temporarily unavailable. Please try again.")

        # Log conversation
        conversation = AIConversation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            assistant_type=AIConversation.AssistantType.PRODUCT_SEARCH,
            title=query[:100],
        )
        AIMessage.objects.create(
            conversation=conversation, role="USER", content=query
        )
        AIMessage.objects.create(
            conversation=conversation, role="ASSISTANT",
            content=ai_text,
            referenced_products=[str(p.id) for p in matched_products],
            disclaimer_shown=True,
            groq_model=settings.GROQ_MODEL,
            tokens_used=tokens_used,
        )

        from products.serializers import ProductListSerializer
        return success_response({
            "query": query,
            "ai_response": ai_text + MEDICAL_DISCLAIMER,
            "products": ProductListSerializer(
                matched_products, many=True, context={"request": request}
            ).data,
            "conversation_id": str(conversation.id),
        })


# ── 2. Health Information Assistant ──────────────────────────────────────────

class HealthInfoView(APIView):
    """
    Answers questions about medicine usage, side effects, interactions.
    Always appends the medical disclaimer — this is a regulatory requirement.
    """
    throttle_classes = [AIRateThrottle, AnonRateThrottle]
    permission_classes = [AllowAny]

    @extend_schema(tags=["AI Assistant"])
    def post(self, request):
        question = request.data.get("question", "").strip()
        conversation_id = request.data.get("conversation_id")  # For multi-turn chat

        if not question:
            return error_response("Question is required.")
        if len(question) > 600:
            return error_response("Question too long.")

        system_prompt = """You are a knowledgeable pharmacy information assistant.
You provide clear, accurate information about:
- Medicine usage and instructions
- Side effects and precautions  
- Drug storage requirements
- General health questions

Rules you MUST follow:
1. Never recommend specific dosages for individual patients
2. Always advise consulting a doctor or pharmacist for personal medical decisions
3. For prescription medicines, emphasize the need for a valid prescription
4. Be accurate, concise, and empathetic
5. Do not diagnose medical conditions
"""

        # Build conversation history for multi-turn support
        messages = [{"role": "system", "content": system_prompt}]
        if conversation_id:
            try:
                conv = AIConversation.objects.get(
                    id=conversation_id,
                    assistant_type=AIConversation.AssistantType.HEALTH_INFO,
                )
                history = conv.messages.filter(role__in=["USER", "ASSISTANT"]).order_by("created_at")[:10]
                for msg in history:
                    messages.append({
                        "role": msg.role.lower(),
                        "content": msg.content,
                    })
            except AIConversation.DoesNotExist:
                conversation_id = None

        messages.append({"role": "user", "content": question})

        try:
            client = get_groq_client()
            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages,
                max_tokens=500,
                temperature=0.4,
            )
            ai_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
        except Exception as e:
            logger.error("Groq API error (health info): %s", str(e))
            return error_response("AI service temporarily unavailable. Please try again.")

        # Save/continue conversation
        if not conversation_id:
            conv = AIConversation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                assistant_type=AIConversation.AssistantType.HEALTH_INFO,
                title=question[:100],
            )
        AIMessage.objects.create(conversation=conv, role="USER", content=question)
        AIMessage.objects.create(
            conversation=conv, role="ASSISTANT",
            content=ai_text,
            disclaimer_shown=True,
            groq_model=settings.GROQ_MODEL,
            tokens_used=tokens_used,
        )

        return success_response({
            "question": question,
            "answer": ai_text + MEDICAL_DISCLAIMER,
            "conversation_id": str(conv.id),
        })


# ── 3. Product Recommendation Engine ─────────────────────────────────────────

class ProductRecommendationView(APIView):
    """
    AI-powered "what else might help" — takes a condition or product name
    and recommends related products from our catalog.
    """
    throttle_classes = [AIRateThrottle, AnonRateThrottle]
    permission_classes = [AllowAny]

    @extend_schema(tags=["AI Assistant"])
    def post(self, request):
        condition_or_product = request.data.get("query", "").strip()
        if not condition_or_product:
            return error_response("Query is required.")

        # Fetch a sample of relevant products to give the AI context
        products = Product.objects.filter(is_active=True).filter(
            description__icontains=condition_or_product
        ) | Product.objects.filter(
            is_active=True, categories__name__icontains=condition_or_product
        )
        products = products.distinct().select_related("brand").prefetch_related("images")[:10]
        product_context = build_product_context(products)

        system_prompt = f"""You are a pharmacy recommendation engine.
Given a health condition or product the customer is interested in, recommend the most appropriate products from our catalog.

Available products:
{product_context}

Instructions:
- Recommend 3-5 most relevant products from the list above
- Explain briefly why each is relevant (1 sentence)
- Group by primary/supporting products if applicable
- Always note which products require a prescription
- Do NOT invent products not in the catalog
- Keep total response under 250 words
"""
        try:
            client = get_groq_client()
            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Recommend products for: {condition_or_product}"},
                ],
                max_tokens=450,
                temperature=0.35,
            )
            ai_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
        except Exception as e:
            logger.error("Groq API error (recommendation): %s", str(e))
            return error_response("AI service temporarily unavailable. Please try again.")

        conversation = AIConversation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            assistant_type=AIConversation.AssistantType.RECOMMENDATION,
            title=condition_or_product[:100],
        )
        AIMessage.objects.create(conversation=conversation, role="USER", content=condition_or_product)
        AIMessage.objects.create(
            conversation=conversation, role="ASSISTANT",
            content=ai_text,
            referenced_products=[str(p.id) for p in products],
            disclaimer_shown=True,
            groq_model=settings.GROQ_MODEL,
            tokens_used=tokens_used,
        )

        from products.serializers import ProductListSerializer
        return success_response({
            "query": condition_or_product,
            "recommendations": ai_text + MEDICAL_DISCLAIMER,
            "products": ProductListSerializer(
                products, many=True, context={"request": request}
            ).data,
            "conversation_id": str(conversation.id),
        })

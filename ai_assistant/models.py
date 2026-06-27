from django.db import models

from core.models import BaseModel
from users.models import User


class AIConversation(BaseModel):
    """
    Groups messages into a session. Separate from a generic chat model
    because each conversation is scoped to one of three distinct AI
    features, which affects system prompting and disclaimer requirements
    downstream in the API layer.
    """

    class AssistantType(models.TextChoices):
        PRODUCT_SEARCH = "PRODUCT_SEARCH", "AI Medicine Search Assistant"
        HEALTH_INFO = "HEALTH_INFO", "AI Health Information Assistant"
        RECOMMENDATION = "RECOMMENDATION", "AI Product Recommendation Engine"

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ai_conversations", null=True, blank=True
    )
    session_key = models.CharField(max_length=64, blank=True, db_index=True)
    assistant_type = models.CharField(max_length=20, choices=AssistantType.choices, db_index=True)
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "assistant_type"])]

    def __str__(self):
        return f"{self.assistant_type} - {self.user or self.session_key}"


class AIMessage(BaseModel):
    class Role(models.TextChoices):
        USER = "USER", "User"
        ASSISTANT = "ASSISTANT", "Assistant"
        SYSTEM = "SYSTEM", "System"

    conversation = models.ForeignKey(AIConversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=Role.choices)
    content = models.TextField()
    # Structured data the AI returned alongside its text reply — e.g. matched
    # product IDs for search, recommended product IDs for the recommendation
    # engine. Keeps the frontend from having to re-parse free text.
    referenced_products = models.JSONField(default=list, blank=True)
    disclaimer_shown = models.BooleanField(
        default=False,
        help_text="Whether the mandatory medical disclaimer was attached to this message"
    )
    groq_model = models.CharField(max_length=100, blank=True)
    tokens_used = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"

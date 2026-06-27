from rest_framework.permissions import AllowAny
from rest_framework import generics
from drf_spectacular.utils import extend_schema

from core.responses import success_response, EnvelopeMixin
from core.pagination import StandardPagination
from rest_framework.views import APIView
from .models import Blog, FAQ
from rest_framework import serializers as drf_serializers


class BlogSerializer(drf_serializers.ModelSerializer):
    author_name = drf_serializers.CharField(source="author.get_full_name", default=None)
    category_name = drf_serializers.CharField(source="category.name", default=None)

    class Meta:
        model = Blog
        fields = ("id", "title", "slug", "author_name", "category_name",
                  "featured_image", "excerpt", "content", "published_at",
                  "view_count", "tags", "meta_title", "meta_description")


class FAQSerializer(drf_serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("id", "question", "answer", "category", "display_order")


class BlogListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardPagination
    search_fields = ["title", "excerpt", "content"]

    @extend_schema(tags=["Content"])
    def get_queryset(self):
        return Blog.objects.filter(
            is_active=True, status="PUBLISHED"
        ).select_related("author", "category").order_by("-published_at")


class BlogDetailView(EnvelopeMixin, generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @extend_schema(tags=["Content"])
    def get_queryset(self):
        return Blog.objects.filter(is_active=True, status="PUBLISHED")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=["view_count"])
        return success_response(self.get_serializer(instance).data)


class FAQListView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=["Content"])
    def get(self, request):
        faqs = FAQ.objects.filter(is_active=True).order_by("category", "display_order")
        grouped = {}
        for faq in faqs:
            cat = faq.get_category_display()
            grouped.setdefault(cat, []).append(FAQSerializer(faq).data)
        return success_response(grouped)

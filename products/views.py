from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from core.permissions import IsAdmin, IsOwnerOrAdmin
from core.responses import success_response, error_response, created_response, EnvelopeMixin
from core.pagination import StandardPagination
from .models import Category, Brand, Manufacturer, Product, Review
from .serializers import (
    CategorySerializer, BrandSerializer, ManufacturerSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductWriteSerializer,
    ReviewSerializer,
)
from .filters import ProductFilter


# ── Categories ───────────────────────────────────────────────────────────────

class CategoryListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Categories"])
    def get_queryset(self):
        # Top-level categories only (children nested via serializer)
        return Category.objects.filter(is_active=True, parent__isnull=True).order_by("display_order")


class FeaturedCategoriesView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Categories"])
    def get_queryset(self):
        return Category.objects.filter(is_active=True, is_featured=True).order_by("display_order")


# ── Products ─────────────────────────────────────────────────────────────────

class ProductListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filterset_class = ProductFilter
    search_fields = ["name", "generic_name", "sku", "brand__name", "description"]
    ordering_fields = ["price", "average_rating", "created_at", "name"]
    ordering = ["-created_at"]
    pagination_class = StandardPagination

    @extend_schema(
        tags=["Products"],
        parameters=[
            OpenApiParameter("search", str, description="Search name, generic name, SKU"),
            OpenApiParameter("min_price", float),
            OpenApiParameter("max_price", float),
            OpenApiParameter("category", str, description="Category slug"),
            OpenApiParameter("in_stock", bool),
            OpenApiParameter("requires_prescription", bool),
        ]
    )
    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True)
            .select_related("brand", "manufacturer")
            .prefetch_related("images", "categories")
        )


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @extend_schema(tags=["Products"])
    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True)
            .select_related("brand", "manufacturer", "inventory")
            .prefetch_related("images", "categories")
        )


class FeaturedProductsView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Products"])
    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True, is_featured=True)
            .select_related("brand")
            .prefetch_related("images", "categories")
        )[:12]


class BestSellersView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Products"])
    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True, is_best_seller=True)
            .select_related("brand")
            .prefetch_related("images", "categories")
        )[:12]


class RecentProductsView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Products"])
    def get_queryset(self):
        return (
            Product.objects
            .filter(is_active=True)
            .select_related("brand")
            .prefetch_related("images", "categories")
            .order_by("-created_at")
        )[:12]


class RelatedProductsView(EnvelopeMixin, generics.ListAPIView):
    """Returns products sharing at least one category with the given product."""
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Products"])
    def get_queryset(self):
        slug = self.kwargs["slug"]
        try:
            product = Product.objects.get(slug=slug, is_active=True)
            category_ids = product.categories.values_list("id", flat=True)
            return (
                Product.objects
                .filter(is_active=True, categories__in=category_ids)
                .exclude(id=product.id)
                .distinct()
                .select_related("brand")
                .prefetch_related("images", "categories")
            )[:8]
        except Product.DoesNotExist:
            return Product.objects.none()


# ── Reviews ──────────────────────────────────────────────────────────────────

class ProductReviewListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    @extend_schema(tags=["Reviews"])
    def get_queryset(self):
        return Review.objects.filter(
            product__slug=self.kwargs["slug"], is_approved=True
        ).select_related("user")

    def create(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs["slug"], is_active=True).first()
        if not product:
            return error_response("Product not found.", status_code=status.HTTP_404_NOT_FOUND)

        if Review.objects.filter(product=product, user=request.user).exists():
            return error_response("You have already reviewed this product.")

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Review submission failed.", serializer.errors)

        review = serializer.save(product=product)

        # Recalculate denormalized rating aggregate
        all_reviews = Review.objects.filter(product=product, is_approved=True)
        count = all_reviews.count()
        avg = sum(r.rating for r in all_reviews) / count if count else 0
        product.review_count = count
        product.average_rating = round(avg, 2)
        product.save(update_fields=["review_count", "average_rating"])

        return created_response(self.get_serializer(review).data, "Review submitted.")


# ── Brands & Manufacturers ───────────────────────────────────────────────────

class BrandListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Products"])
    def get_queryset(self):
        return Brand.objects.filter(is_active=True).order_by("name")


class ManufacturerListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = ManufacturerSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Products"])
    def get_queryset(self):
        return Manufacturer.objects.filter(is_active=True).order_by("name")


# ── Admin product management ─────────────────────────────────────────────────

class AdminProductListCreateView(EnvelopeMixin, generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination
    filterset_class = ProductFilter
    search_fields = ["name", "sku", "generic_name"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductWriteSerializer
        return ProductListSerializer

    @extend_schema(tags=["Admin - Products"])
    def get_queryset(self):
        return Product.objects.all().select_related("brand", "manufacturer").prefetch_related("images", "categories")

    def create(self, request, *args, **kwargs):
        serializer = ProductWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Product creation failed.", serializer.errors)
        product = serializer.save()
        return created_response(ProductDetailSerializer(product).data, "Product created.")


class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = Product.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductWriteSerializer
        return ProductDetailSerializer

    @extend_schema(tags=["Admin - Products"])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = ProductWriteSerializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error_response("Update failed.", serializer.errors)
        product = serializer.save()
        return success_response(ProductDetailSerializer(product).data, "Product updated.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return success_response(message="Product deactivated.")

from django.db.models import Prefetch

from rest_framework import generics

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from django_filters.rest_framework import (
    DjangoFilterBackend,
)

from products.models import (
    Product,
    ProductImage,
)

from products.api.serializers import (
    ProductListSerializer,
)

from products.api.pagination import (
    ProductPagination,
)

from products.api.filters import (
    ProductFilter,
)


class ProductListAPIView(
    generics.ListAPIView,
):
    """
    GET /api/products/
    """

    serializer_class = (
        ProductListSerializer
    )

    pagination_class = (
        ProductPagination
    )

    filter_backends = (

        DjangoFilterBackend,

        SearchFilter,

        OrderingFilter,

    )

    filterset_class = (
        ProductFilter
    )

    search_fields = (

        "name",

        "generic_name",

        "sku",

        "brand__name",

        "manufacturer__name",

    )

    ordering_fields = (

        "price",

        "created_at",

        "average_rating",

        "review_count",

        "name",

    )

    ordering = (

        "-created_at",
    )

    def get_queryset(self):

        return (
            Product.objects.filter(
                is_active=True,
            )

            .select_related(
                "brand",
                "manufacturer",
            )

            .prefetch_related(

                "categories",

                Prefetch(
                    "images",
                    queryset=ProductImage.objects.order_by(
                        "-is_primary",
                        "display_order",
                    ),
                ),
            )

            .distinct()
        )
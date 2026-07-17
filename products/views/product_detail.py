from django.db.models import Prefetch

from rest_framework import generics

from products.models import (
    Product,
    ProductImage,
)

from products.api.serializers import (
    ProductDetailSerializer,
)


class ProductDetailAPIView(
    generics.RetrieveAPIView,
):
    """
    GET /products/<slug>/
    """

    serializer_class = (
        ProductDetailSerializer
    )

    lookup_field = "slug"

    def get_queryset(self):

        return (

            Product.objects.filter(
                is_active=True,
            )

            .select_related(
                "brand",
                "manufacturer",
                "inventory",
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

                "reviews",
            )
        )
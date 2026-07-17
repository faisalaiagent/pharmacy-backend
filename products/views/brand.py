from rest_framework import generics

from products.models import Brand

from products.api.serializers import BrandSerializer


class BrandListAPIView(
    generics.ListAPIView,
):

    serializer_class = BrandSerializer

    queryset = (
        Brand.objects.select_related(
            "manufacturer",
        )
    )
from rest_framework import generics

from products.models import Manufacturer

from products.api.serializers import ManufacturerSerializer


class ManufacturerListAPIView(
    generics.ListAPIView,
):

    serializer_class = (
        ManufacturerSerializer
    )

    queryset = (
        Manufacturer.objects.filter(
            is_active=True,
        )
    )
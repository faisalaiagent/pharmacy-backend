from rest_framework import generics

from products.models import Category

from products.api.serializers import CategorySerializer


class CategoryListAPIView(
    generics.ListAPIView,
):

    serializer_class = CategorySerializer

    queryset = (
        Category.objects.filter(
            is_active=True,
        )
    )
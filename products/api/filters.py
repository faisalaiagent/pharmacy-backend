import django_filters

from products.models import Product


class ProductFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(
        field_name="categories__slug",
        lookup_expr="iexact",
    )

    brand = django_filters.CharFilter(
        field_name="brand__slug",
        lookup_expr="iexact",
    )

    manufacturer = django_filters.CharFilter(
        field_name="manufacturer__slug",
        lookup_expr="iexact",
    )

    generic = django_filters.CharFilter(
        field_name="generic_name",
        lookup_expr="icontains",
    )

    prescription = django_filters.BooleanFilter(
        field_name="requires_prescription",
    )

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
    )

    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
    )

    class Meta:

        model = Product

        fields = []
import django_filters
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="categories__slug", lookup_expr="exact")
    brand = django_filters.CharFilter(field_name="brand__slug", lookup_expr="exact")
    manufacturer = django_filters.CharFilter(field_name="manufacturer__slug", lookup_expr="exact")
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")
    requires_prescription = django_filters.BooleanFilter()
    product_type = django_filters.CharFilter(lookup_expr="exact")
    is_featured = django_filters.BooleanFilter()
    is_best_seller = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = ["product_type", "requires_prescription", "is_featured",
                  "is_best_seller", "stock_status"]

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.exclude(stock_status="OUT_OF_STOCK").exclude(stock_status="DISCONTINUED")
        return queryset

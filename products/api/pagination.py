from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """
    Standard pagination for product listings.
    """

    page_size = 12

    page_size_query_param = "page_size"

    max_page_size = 100

    page_query_param = "page"

    REST_FRAMEWORK = {

        "DEFAULT_FILTER_BACKENDS": [

            "django_filters.rest_framework.DjangoFilterBackend",

            "rest_framework.filters.SearchFilter",

            "rest_framework.filters.OrderingFilter",

        ],
    }
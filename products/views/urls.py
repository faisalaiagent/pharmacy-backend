from django.urls import path

from products.api.views.product_list import (
    ProductListAPIView,
)

from products.api.views.product_detail import (
    ProductDetailAPIView,
)

from products.api.views.category import (
    CategoryListAPIView,
)

from products.api.views.brand import (
    BrandListAPIView,
)

from products.api.views.manufacturer import (
    ManufacturerListAPIView,
)

urlpatterns = [

    path(
        "products/",
        ProductListAPIView.as_view(),
        name="product-list",
    ),

    path(
        "products/<slug:slug>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),

    path(
        "categories/",
        CategoryListAPIView.as_view(),
        name="category-list",
    ),

    path(
        "brands/",
        BrandListAPIView.as_view(),
        name="brand-list",
    ),

    path(
        "manufacturers/",
        ManufacturerListAPIView.as_view(),
        name="manufacturer-list",
    ),
]
from django.urls import path
from .views import (
    CategoryListView, FeaturedCategoriesView,
    ProductListView, ProductDetailView,
    FeaturedProductsView, BestSellersView, RecentProductsView, RelatedProductsView,
    ProductReviewListView,
    BrandListView, ManufacturerListView,
    AdminProductListCreateView, AdminProductDetailView,
)

app_name = "products"

urlpatterns = [
    # Public catalog
    path("", ProductListView.as_view(), name="product-list"),
    path("featured/", FeaturedProductsView.as_view(), name="featured"),
    path("best-sellers/", BestSellersView.as_view(), name="best-sellers"),
    path("recent/", RecentProductsView.as_view(), name="recent"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
    path("<slug:slug>/related/", RelatedProductsView.as_view(), name="related"),
    path("<slug:slug>/reviews/", ProductReviewListView.as_view(), name="reviews"),

    # Categories
    path("categories/all/", CategoryListView.as_view(), name="category-list"),
    path("categories/featured/", FeaturedCategoriesView.as_view(), name="category-featured"),

    # Brands & Manufacturers
    path("brands/all/", BrandListView.as_view(), name="brand-list"),
    path("manufacturers/all/", ManufacturerListView.as_view(), name="manufacturer-list"),

    # Admin
    path("admin/products/", AdminProductListCreateView.as_view(), name="admin-list"),
    path("admin/products/<uuid:id>/", AdminProductDetailView.as_view(), name="admin-detail"),
]

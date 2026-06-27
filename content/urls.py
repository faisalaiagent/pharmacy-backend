from django.urls import path
from .views import BlogListView, BlogDetailView, FAQListView

app_name = "content"

urlpatterns = [
    path("blog/", BlogListView.as_view(), name="blog-list"),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
    path("faqs/", FAQListView.as_view(), name="faq-list"),
]

from django.urls import path
from .views import MedicineSearchView, HealthInfoView, ProductRecommendationView

app_name = "ai_assistant"

urlpatterns = [
    path("search/", MedicineSearchView.as_view(), name="medicine-search"),
    path("health-info/", HealthInfoView.as_view(), name="health-info"),
    path("recommend/", ProductRecommendationView.as_view(), name="recommend"),
]

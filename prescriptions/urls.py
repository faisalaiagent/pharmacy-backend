from django.urls import path
from .views import (
    UploadPrescriptionView, CustomerPrescriptionListView, CustomerPrescriptionDetailView,
    PharmacistPrescriptionQueueView, PharmacistClaimPrescriptionView, PharmacistReviewPrescriptionView,
    AdminPrescriptionListView, AdminAssignPharmacistView,
)

app_name = "prescriptions"

urlpatterns = [
    # Customer
    path("", CustomerPrescriptionListView.as_view(), name="prescription-list"),
    path("upload/", UploadPrescriptionView.as_view(), name="upload"),
    path("<uuid:pk>/", CustomerPrescriptionDetailView.as_view(), name="detail"),

    # Pharmacist
    path("pharmacist/queue/", PharmacistPrescriptionQueueView.as_view(), name="pharmacist-queue"),
    path("pharmacist/<uuid:pk>/claim/", PharmacistClaimPrescriptionView.as_view(), name="pharmacist-claim"),
    path("pharmacist/<uuid:pk>/review/", PharmacistReviewPrescriptionView.as_view(), name="pharmacist-review"),

    # Admin
    path("admin/", AdminPrescriptionListView.as_view(), name="admin-list"),
    path("admin/<uuid:pk>/assign/", AdminAssignPharmacistView.as_view(), name="admin-assign"),
]

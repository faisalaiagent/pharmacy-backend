import logging
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.permissions import IsPharmacist, IsAdmin, IsAdminOrPharmacist, IsOwnerOrAdmin
from core.responses import success_response, error_response, created_response, EnvelopeMixin
from core.pagination import StandardPagination
from notifications.models import Notification
from .models import Prescription, PrescriptionReview
from .serializers import (
    PrescriptionSerializer, UploadPrescriptionSerializer, PharmacistReviewSerializer
)

logger = logging.getLogger(__name__)

MEDICAL_DISCLAIMER = (
    "⚠️ MEDICAL DISCLAIMER: This platform does not provide medical advice. "
    "All prescription medicines require a valid prescription from a licensed doctor. "
    "Consult a qualified healthcare professional before taking any medication."
)


class UploadPrescriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=UploadPrescriptionSerializer, tags=["Prescriptions"])
    def post(self, request):
        serializer = UploadPrescriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Upload failed.", serializer.errors)

        prescription = Prescription.objects.create(
            user=request.user,
            **serializer.validated_data
        )

        # Notify admins of new prescription needing review
        Notification.objects.create(
            notification_type="SYSTEM",
            title="New Prescription Submitted",
            message=f"Customer {request.user.email} uploaded a prescription for review.",
            is_admin_alert=True,
            metadata={"prescription_id": str(prescription.id)}
        )

        logger.info("Prescription uploaded by %s: %s", request.user.email, prescription.id)
        data = PrescriptionSerializer(prescription).data
        data["disclaimer"] = MEDICAL_DISCLAIMER
        return created_response(data, "Prescription uploaded and submitted for review.")


class CustomerPrescriptionListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    @extend_schema(tags=["Prescriptions"])
    def get_queryset(self):
        return Prescription.objects.filter(user=self.request.user).prefetch_related(
            "items", "reviews"
        ).order_by("-created_at")


class CustomerPrescriptionDetailView(EnvelopeMixin, generics.RetrieveAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Prescriptions"])
    def get_queryset(self):
        return Prescription.objects.filter(user=self.request.user)


# ── Pharmacist views ──────────────────────────────────────────────────────────

class PharmacistPrescriptionQueueView(EnvelopeMixin, generics.ListAPIView):
    """Returns PENDING prescriptions assigned to this pharmacist or unassigned."""
    serializer_class = PrescriptionSerializer
    permission_classes = [IsPharmacist]
    pagination_class = StandardPagination

    @extend_schema(tags=["Pharmacist"])
    def get_queryset(self):
        return Prescription.objects.filter(
            status__in=["PENDING", "UNDER_REVIEW"],
        ).select_related("user").prefetch_related("items", "reviews").order_by("created_at")


class PharmacistClaimPrescriptionView(APIView):
    """Pharmacist self-assigns a prescription to start the review."""
    permission_classes = [IsPharmacist]

    @extend_schema(tags=["Pharmacist"])
    def post(self, request, pk):
        try:
            prescription = Prescription.objects.get(pk=pk, status="PENDING")
        except Prescription.DoesNotExist:
            return error_response("Prescription not found or already under review.",
                                  status_code=status.HTTP_404_NOT_FOUND)

        prescription.assigned_pharmacist = request.user
        prescription.status = Prescription.Status.UNDER_REVIEW
        prescription.save(update_fields=["assigned_pharmacist", "status"])

        return success_response(
            PrescriptionSerializer(prescription).data,
            "Prescription claimed for review."
        )


class PharmacistReviewPrescriptionView(APIView):
    """Pharmacist submits approve/reject/clarification decision."""
    permission_classes = [IsPharmacist]

    @extend_schema(request=PharmacistReviewSerializer, tags=["Pharmacist"])
    def post(self, request, pk):
        try:
            prescription = Prescription.objects.get(
                pk=pk,
                assigned_pharmacist=request.user,
                status=Prescription.Status.UNDER_REVIEW,
            )
        except Prescription.DoesNotExist:
            return error_response("Prescription not found or not assigned to you.",
                                  status_code=status.HTTP_404_NOT_FOUND)

        serializer = PharmacistReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Review submission failed.", serializer.errors)

        decision = serializer.validated_data["decision"]

        # Create immutable audit record
        PrescriptionReview.objects.create(
            prescription=prescription,
            pharmacist=request.user,
            **serializer.validated_data,
        )

        # Update prescription status
        if decision == "APPROVED":
            prescription.status = Prescription.Status.APPROVED
        elif decision == "REJECTED":
            prescription.status = Prescription.Status.REJECTED
        # NEEDS_CLARIFICATION leaves it UNDER_REVIEW
        prescription.save(update_fields=["status"])

        # Notify customer
        notif_type = "PRESCRIPTION_APPROVED" if decision == "APPROVED" else "PRESCRIPTION_REJECTED"
        Notification.objects.create(
            user=prescription.user,
            notification_type=notif_type,
            title=f"Prescription {decision.title()}",
            message=serializer.validated_data.get("comments", f"Your prescription has been {decision.lower()}."),
            metadata={"prescription_id": str(prescription.id)},
        )

        logger.info("Prescription %s %s by pharmacist %s", prescription.id, decision, request.user.email)
        return success_response(PrescriptionSerializer(prescription).data,
                                f"Prescription {decision.lower()} successfully.")


# ── Admin views ───────────────────────────────────────────────────────────────

class AdminPrescriptionListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAdmin]
    pagination_class = StandardPagination
    filterset_fields = ["status", "file_type"]
    search_fields = ["user__email", "patient_name", "doctor_name"]

    @extend_schema(tags=["Admin - Prescriptions"])
    def get_queryset(self):
        return Prescription.objects.all().select_related(
            "user", "assigned_pharmacist"
        ).prefetch_related("items", "reviews").order_by("-created_at")


class AdminAssignPharmacistView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(tags=["Admin - Prescriptions"])
    def post(self, request, pk):
        pharmacist_id = request.data.get("pharmacist_id")
        try:
            from users.models import User
            pharmacist = User.objects.get(id=pharmacist_id, role="PHARMACIST")
            prescription = Prescription.objects.get(pk=pk)
        except Exception:
            return error_response("Invalid pharmacist or prescription.")

        prescription.assigned_pharmacist = pharmacist
        prescription.status = Prescription.Status.UNDER_REVIEW
        prescription.save(update_fields=["assigned_pharmacist", "status"])
        return success_response(message=f"Prescription assigned to {pharmacist.get_full_name()}.")

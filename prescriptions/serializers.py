from rest_framework import serializers
from .models import Prescription, PrescriptionItem, PrescriptionReview


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = ("id", "product", "medicine_name", "dosage", "quantity", "instructions")


class PrescriptionReviewSerializer(serializers.ModelSerializer):
    pharmacist_name = serializers.CharField(source="pharmacist.get_full_name", default=None)

    class Meta:
        model = PrescriptionReview
        fields = ("id", "pharmacist_name", "decision", "comments", "rejection_reason", "created_at")


class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)
    reviews = PrescriptionReviewSerializer(many=True, read_only=True)
    uploaded_by = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Prescription
        fields = ("id", "uploaded_by", "file_url", "file_type", "file_size_bytes",
                  "patient_name", "doctor_name", "doctor_license_number", "issued_date",
                  "customer_notes", "status", "assigned_pharmacist",
                  "valid_until", "items", "reviews", "created_at")
        read_only_fields = ("id", "uploaded_by", "status", "assigned_pharmacist", "created_at")


class UploadPrescriptionSerializer(serializers.Serializer):
    """Customer submits a Cloudinary/S3 URL after uploading on frontend."""
    file_url = serializers.URLField()
    file_type = serializers.ChoiceField(choices=["IMAGE", "PDF"])
    file_size_bytes = serializers.IntegerField(min_value=1)
    patient_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    doctor_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    doctor_license_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    issued_date = serializers.DateField(required=False, allow_null=True)
    customer_notes = serializers.CharField(required=False, allow_blank=True)


class PharmacistReviewSerializer(serializers.Serializer):
    decision = serializers.ChoiceField(choices=PrescriptionReview.Decision.choices)
    comments = serializers.CharField(required=False, allow_blank=True)
    rejection_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs["decision"] == "REJECTED" and not attrs.get("rejection_reason"):
            raise serializers.ValidationError(
                {"rejection_reason": "A reason is required when rejecting a prescription."}
            )
        return attrs

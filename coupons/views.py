from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.permissions import IsAdmin
from core.responses import success_response, error_response
from .models import Coupon
from rest_framework import serializers as drf_serializers


class CouponSerializer(drf_serializers.ModelSerializer):
    is_valid_now = drf_serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ("id", "code", "discount_type", "discount_value", "max_discount_amount",
                  "min_order_amount", "usage_limit", "times_used", "valid_from",
                  "valid_until", "is_active", "is_valid_now")

    def get_is_valid_now(self, obj):
        return obj.is_valid()


class ValidateCouponView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Coupons"])
    def post(self, request):
        code = request.data.get("code", "").strip().upper()
        if not code:
            return error_response("Coupon code is required.")
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return error_response("Invalid coupon code.")
        if not coupon.is_valid():
            return error_response("Coupon is expired or no longer valid.")
        return success_response(CouponSerializer(coupon).data, "Coupon is valid!")


class AdminCouponListCreateView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(tags=["Admin - Coupons"])
    def get(self, request):
        coupons = Coupon.objects.all().order_by("-created_at")
        return success_response(CouponSerializer(coupons, many=True).data)

    @extend_schema(tags=["Admin - Coupons"])
    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Coupon creation failed.", serializer.errors)
        coupon = serializer.save()
        return success_response(CouponSerializer(coupon).data, "Coupon created.")

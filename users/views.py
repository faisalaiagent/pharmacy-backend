import logging
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiParameter

from core.permissions import IsAdmin, IsOwnerOrAdmin
from core.responses import success_response, error_response, created_response, EnvelopeMixin
from .models import User, Address, PharmacistProfile
from .serializers import (
    RegisterSerializer, LoginSerializer, UserTokenSerializer,
    UserProfileSerializer, ChangePasswordSerializer, AddressSerializer,
    PharmacistProfileSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: UserTokenSerializer},
                   tags=["Authentication"])
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Registration failed.", serializer.errors)

        user = serializer.save()
        token_data = UserTokenSerializer(user).data
        logger.info("New user registered: %s", user.email)
        return created_response(token_data, "Registration successful. Welcome!")


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: UserTokenSerializer},
                   tags=["Authentication"])
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            # Track failed attempts for account lockout
            email = request.data.get("email", "")
            try:
                user = User.objects.get(email=email)
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    from datetime import timedelta
                    user.locked_until = timezone.now() + timedelta(minutes=30)
                user.save(update_fields=["failed_login_attempts", "locked_until"])
            except User.DoesNotExist:
                pass
            return error_response("Login failed.", serializer.errors, status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data["user"]
        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_ip = request.client_ip if hasattr(request, "client_ip") else None
        user.save(update_fields=["failed_login_attempts", "locked_until", "last_login_ip"])

        token_data = UserTokenSerializer(user).data
        return success_response(token_data, f"Welcome back, {user.first_name or user.username}!")


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Authentication"])
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return success_response(message="Logged out successfully.")
        except TokenError:
            return error_response("Invalid or expired token.")


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Profile"])
    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return success_response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error_response("Profile update failed.", serializer.errors)
        serializer.save()
        return success_response(serializer.data, "Profile updated successfully.")


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=ChangePasswordSerializer, tags=["Profile"])
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error_response("Password change failed.", serializer.errors)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        update_session_auth_hash(request, request.user)
        return success_response(message="Password changed successfully.")


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=PasswordResetRequestSerializer, tags=["Authentication"])
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Invalid request.", serializer.errors)

        email = serializer.validated_data["email"]
        # Always return success even if email doesn't exist (security: don't leak emails)
        try:
            user = User.objects.get(email=email, is_active=True)
            # TODO: generate token, send email via Celery task
            # For now, log for development
            logger.info("Password reset requested for: %s", email)
        except User.DoesNotExist:
            pass

        return success_response(
            message="If an account exists with that email, a reset link has been sent."
        )


class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Address book is small — no pagination needed

    @extend_schema(tags=["Addresses"])
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).order_by("-is_default", "-created_at")

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Address creation failed.", serializer.errors)
        serializer.save()
        return created_response(serializer.data, "Address added successfully.")


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    @extend_schema(tags=["Addresses"])
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        return success_response(self.get_serializer(self.get_object()).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error_response("Address update failed.", serializer.errors)
        serializer.save()
        return success_response(serializer.data, "Address updated.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message="Address deleted.")


class SetDefaultAddressView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["Addresses"])
    def post(self, request, pk):
        try:
            address = Address.objects.get(pk=pk, user=request.user)
            address.is_default = True
            address.save()
            return success_response(message="Default address updated.")
        except Address.DoesNotExist:
            return error_response("Address not found.", status_code=status.HTTP_404_NOT_FOUND)


# ── Admin-only views ─────────────────────────────────────────────────────────

class UserListView(EnvelopeMixin, generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdmin]
    filterset_fields = ["role", "is_active", "email_verified"]
    search_fields = ["email", "username", "first_name", "last_name"]

    @extend_schema(tags=["Admin - Users"])
    def get_queryset(self):
        return User.objects.all().order_by("-created_at")


class UserDetailAdminView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.all()

    @extend_schema(tags=["Admin - Users"])
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return error_response("Update failed.", serializer.errors)
        serializer.save()
        return success_response(serializer.data, "User updated.")


class VerifyPharmacistView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(tags=["Admin - Users"])
    def post(self, request, pk):
        try:
            profile = PharmacistProfile.objects.select_related("user").get(pk=pk)
            profile.is_verified = True
            profile.verified_at = timezone.now()
            profile.verified_by = request.user
            profile.save(update_fields=["is_verified", "verified_at", "verified_by"])
            return success_response(message=f"Pharmacist {profile.user.get_full_name()} verified.")
        except PharmacistProfile.DoesNotExist:
            return error_response("Pharmacist profile not found.", status_code=status.HTTP_404_NOT_FOUND)

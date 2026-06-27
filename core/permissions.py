"""
Reusable DRF permission classes.
Every view in the platform uses one of these rather than ad-hoc inline
permission logic, keeping RBAC centralised and auditable.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "CUSTOMER")


class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role != "PHARMACIST":
            return False
        # Must also have a verified pharmacist profile
        try:
            return request.user.pharmacist_profile.is_verified
        except Exception:
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "ADMIN")


class IsAdminOrPharmacist(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in ("ADMIN", "PHARMACIST")


class IsOwnerOrAdmin(BasePermission):
    """Object-level: only owner or admin can access."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == "ADMIN":
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user


class IsAuthenticatedOrReadOnly(BasePermission):
    """Read-only for anonymous, full access for authenticated."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

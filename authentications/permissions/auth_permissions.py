from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticatedAndEmailVerified(BasePermission):
    """
    Allows access only to authenticated users who are verified.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_verified
        )


class IsAuthenticatedAndEmailNotVerified(BasePermission):
    """
    Allows access only to authenticated users without a verified email.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and not request.user.is_verified
        )


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "seller")


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == "buyer")


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsUserOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user

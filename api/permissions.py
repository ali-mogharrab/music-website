from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return obj == request.user
        except:
            return False

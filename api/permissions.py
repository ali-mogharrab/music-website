from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            return obj == request.user
        except:
            return False


class IsArtistOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        try:
            return request.user.profile.artist in obj.artist.all()
        except:
            return False

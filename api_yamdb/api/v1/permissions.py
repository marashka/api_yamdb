from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                or request.method in SAFE_METHODS)


class IsAdminModAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        return (request.user.is_authenticated
                and (request.user == obj.author
                     or request.user.is_moderator
                     or request.user.is_admin
                     )
                )

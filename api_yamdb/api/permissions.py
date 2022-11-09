from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin or request.user.is_superuser)
# у энд приоритет выше. значит ваше запись эквиваленте ((request.user.is_authenticated and request.user.is_admin) 
# or request.user.is_superuser) а это явно не то что вы задумали.
    def has_object_permission(self, request, view, obj):
# это два разных уровня примишенов. не аутентифицированного срежет верхний примишен. тут можно быть уверенным что юзер аутентифицированного. 
# тут же проверяется доступ уже к конкретному объекту.
# https://www.django-rest-framework.org/api-guide/permissions/
        return (request.user.is_authenticated
                and request.user.is_admin or request.user.is_superuser)


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moderator


class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_user
                or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in SAFE_METHODS)


class IsReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS

from rest_framework import permissions


class IsAuthenticatedOrPostAllowAny(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return super().has_permission(request, view)

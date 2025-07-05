from rest_framework import permissions

class IsOwnerOrIsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to see/edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Superusers can access any object.
        if request.user and request.user.is_superuser:
            return True
        
        # The owner of the object can access it.
        return obj.user == request.user
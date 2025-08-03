from rest_framework.permissions import BasePermission 

class IsOwnerorReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS (read-only)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.owner == request.user  # Assuming Book has an 'owner' field

# ! Not Completed 

from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsObjectUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.user==request.user)
    


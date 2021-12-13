from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsBlogUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.writer.user == request.user

class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.user == request.user
        
class IsNotBlogUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return not obj.writer.user == request.user

class ValidUser(BasePermission):

    def has_permission(self, request, view):
        return str(request.user.profile.id) == view.kwargs['pk']

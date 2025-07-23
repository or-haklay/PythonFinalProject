from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
     Allow only admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.is_superuser

class CommentOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, 'author') and hasattr(obj.author, 'user'):
            return obj.author.user == request.user

        return False
    

class ArticlesPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True
 
        return request.user.is_superuser or request.user.is_staff
    
class TagsPermission(ArticlesPermission):
    """
    Allow admins to write Tags, all users can read
    """


class UserProfilePermission(permissions.BasePermission):
    """
      allow the user and admin to edit, rest can view
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser

class UserLikesPermission(permissions.BasePermission):
    """
      allow the user and admin to edit, rest can view
    """
    def has_object_permission(self, request, view, obj):
        return obj.user.user == request.user or request.user.is_superuser
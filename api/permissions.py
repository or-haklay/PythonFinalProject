from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
     Allow only admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.is_superuser


class IsEditorOrAdmin(permissions.BasePermission):
    """
    Allow editors and admins to access the view.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (request.user.is_superuser or 
                request.user.groups.filter(name__in=['Editors', 'Admin']).exists())


class IsUserOrEditorOrAdmin(permissions.BasePermission):
    """
    Allow users, editors, and admins to access the view.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            print(f"DEBUG: User not authenticated: {request.user}")
            return False
        
        user_groups = list(request.user.groups.values_list('name', flat=True))
        print(f"DEBUG: User {request.user.username} groups: {user_groups}")
        
        is_superuser = request.user.is_superuser
        has_group = request.user.groups.filter(name__in=['Users', 'Editors', 'Admin']).exists()
        
        print(f"DEBUG: Is superuser: {is_superuser}, Has group: {has_group}")
        
        result = is_superuser or has_group
        print(f"DEBUG: Permission result: {result}")
        
        return result

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
 
        return IsUserOrEditorOrAdmin().has_permission(request, view)
    
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


from rest_framework.response import Response
from core.auth import get_token_for_user
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import filters

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serialiazers import (ArticleSerializer, ArticleUserLikesSerializer, UserSerializer, UserProfileSerializer,
                           CommentSerializer,
                           TagSerializer)

from .models import Article, ArticleUserLikes, Tag, UserProfile, Article, Comment, ArticleUserLikes

#from rest_framework.permissions import IsAdminUser

from .permissions import (CommentOwnerOrReadOnly, ArticlesPermission, IsAdmin,
                          TagsPermission, UserLikesPermission, UserProfilePermission,
                          IsEditorOrAdmin, IsUserOrEditorOrAdmin)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [TagsPermission]


class ArticleUserLikesViewSet(ModelViewSet):
    queryset = ArticleUserLikes.objects.all()
    serializer_class = ArticleUserLikesSerializer
    permission_classes = [UserLikesPermission]


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [ArticlesPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'text', 'tags__name']
    
    def create(self, request, *args, **kwargs):
        print(f"DEBUG: Creating article with data: {request.data}")
        print(f"DEBUG: User: {request.user}")
        print(f"DEBUG: User profile: {getattr(request.user, 'userprofile', 'No profile')}")
        return super().create(request, *args, **kwargs)
    
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        print(f"DEBUG: Comments endpoint called by user: {request.user}")
        print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
        print(f"DEBUG: User groups: {list(request.user.groups.values_list('name', flat=True))}")
        
        article = self.get_object()
        if request.method == 'GET':
            comments = Comment.objects.filter(article=article)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            # Check permissions manually
            print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
            print(f"DEBUG: User: {request.user}")
            print(f"DEBUG: User groups: {list(request.user.groups.values_list('name', flat=True))}")
            
            if not request.user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=401)
            
            if not (request.user.is_superuser or 
                   request.user.groups.filter(name__in=['Users', 'Editors', 'Admin']).exists()):
                return Response({'error': 'Permission denied'}, status=403)
            
            print(f"DEBUG: Comment data: {request.data}")
            print(f"DEBUG: Article: {article}")
            print(f"DEBUG: User profile: {request.user.userprofile}")
            
            serializer = CommentSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                print(f"DEBUG: Serializer is valid, saving...")
                serializer.save(article=article, author=request.user.userprofile)
                return Response(serializer.data, status=201)
            else:
                print(f"DEBUG: Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=400)


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserProfilePermission]


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentOwnerOrReadOnly]
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsUserOrEditorOrAdmin]
        else:
            permission_classes = [CommentOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


# checks the username and password against the database:


class AuthViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    @action(methods=['post', 'get'], detail=False)
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        # validation by our rules in UserSerializer and in User:
        # example check that password has at least 8 characters
        serializer.is_valid(raise_exception=True)

        user = serializer.save()  # calls the create method
        jwt = get_token_for_user(user)

        # יוצר פרופיל למשתמש אוטומטית בעת ההרשמה
        UserProfile.objects.get_or_create(user = user)
        
        # מוסיף את המשתמש לקבוצת Users
        from django.contrib.auth.models import Group
        users_group, created = Group.objects.get_or_create(name='Users')
        user.groups.add(users_group)
        
        return Response({'message': 'Registered successfully', 'user':serializer.data, **jwt})



    def list(self, request):
        return Response({
            'login': 'http://127.0.0.1:8000/api/auth/login',
            'register': 'http://127.0.0.1:8000/api/auth/register',
        })
    
    @action(methods=['post', 'get'], detail=False)
    def login(self, request):

        # create the serializer object
        serializer = AuthTokenSerializer(
            data=request.data, context={'request': request}
        )

        # if password!=password -> throw
        serializer.is_valid(raise_exception=True)  # 401

        # get the user from the serializer:
        user = serializer.validated_data['user']

        jwt = get_token_for_user(user)

        return Response(jwt)
    
    @action(methods=['get'], detail=False)
    def auth(self, request):
        """Check if user is authenticated"""
        if request.user.is_authenticated:
            return Response({'authenticated': True, 'user': request.user.username})
        return Response({'authenticated': False}, status=401)
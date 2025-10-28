from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (CommentViewSet, ArticleViewSet, ArticleUserLikesViewSet,
                    UserProfileViewSet, UserViewSet, TagViewSet, AuthViewSet
                    )


router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('auth', AuthViewSet, basename='auth')
router.register('comments', CommentViewSet, basename='comments')
router.register('articles', ArticleViewSet, basename='articles')
router.register('users', UserViewSet, basename='users')
router.register('userprofiles', UserProfileViewSet, basename='userprofiles')
router.register('likes', ArticleUserLikesViewSet, basename='likes')

#המסודר הזה יוצר את הכתובות URL עבור כל ה-ViewSets שנרשמו

urlpatterns = router.urls

# Add specific endpoints for register and login
urlpatterns += [
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
]
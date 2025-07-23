from rest_framework.routers import DefaultRouter

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

#optional: we can add more patterns here:
urlpatterns += [
    
]
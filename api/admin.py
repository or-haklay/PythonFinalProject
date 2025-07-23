from django.contrib import admin

from .models import Comment, UserProfile, Article, Tag, ArticleUserLikes

# Register your models here.

admin.site.register([Comment, UserProfile, Article, Tag, ArticleUserLikes])

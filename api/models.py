from django.core.validators import RegexValidator, MinLengthValidator
from django.contrib.auth.models import User
from django.db import models


# from django.core import validators

class Tag(models.Model):
    # props
    name = models.CharField(unique=True, max_length=32)

    # str representation for the admin panel
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    bio = models.TextField(blank=True, max_length=1000)
    birthdate = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'


# Article status
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('archived', 'Archived')
]


class Article(models.Model):
    # one to many
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE
    )

    title = models.CharField(max_length=100, unique=True, validators=[
        MinLengthValidator(5),
        RegexValidator(regex='^[a-zA-Z].*$')
    ])
    text = models.TextField(validators=[MinLengthValidator(5)])
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return f'{self.title} by {self.author.user.username}'


class Comment(models.Model):
    # one to many
    author = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE
    )
    # one to many
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE
    )
    
    text = models.TextField(max_length=200, validators=[MinLengthValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    reply_to = models.ForeignKey('self',
                                 default=None,
                                 null=True,
                                 blank=True,
                                 on_delete=models.CASCADE
                                 )

    def __str__(self):
        return f'{self.text} by {self.author.user.username}'


# Like options:
LIKE_CHOICES = [
    ('like', 'Like'),
    ('dislike', 'Dislike'),
]


class ArticleUserLikes(models.Model):
    # props:
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    like_type = models.CharField(choices=LIKE_CHOICES, default='like')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'article']

    def __str__(self):
        return f'{self.user.user.username} {self.like_type}d {self.article.title}'
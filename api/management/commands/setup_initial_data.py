from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from api.models import Article, Comment, Tag, UserProfile


class Command(BaseCommand):
    help = 'Set up initial data including user groups and sample content'

    def handle(self, *args, **options):
        # Create user groups
        self.create_groups()
        
        # Create sample users
        self.create_sample_users()
        
        # Create sample tags
        self.create_sample_tags()
        
        # Create sample articles
        self.create_sample_articles()
        
        # Create sample comments
        self.create_sample_comments()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully set up initial data!')
        )

    def create_groups(self):
        # Create groups
        editors_group, created = Group.objects.get_or_create(name='Editors')
        users_group, created = Group.objects.get_or_create(name='Users')
        admin_group, created = Group.objects.get_or_create(name='Admin')
        
        # Get content types for permissions
        article_content_type = ContentType.objects.get_for_model(Article)
        comment_content_type = ContentType.objects.get_for_model(Comment)
        
        # Add permissions to editors group
        editors_group.permissions.add(
            Permission.objects.get(codename='add_article', content_type=article_content_type),
            Permission.objects.get(codename='change_article', content_type=article_content_type),
            Permission.objects.get(codename='delete_article', content_type=article_content_type),
            Permission.objects.get(codename='view_article', content_type=article_content_type),
            Permission.objects.get(codename='delete_comment', content_type=comment_content_type),
        )
        
        # Add permissions to users group
        users_group.permissions.add(
            Permission.objects.get(codename='view_article', content_type=article_content_type),
            Permission.objects.get(codename='add_comment', content_type=comment_content_type),
            Permission.objects.get(codename='view_comment', content_type=comment_content_type),
        )
        
        self.stdout.write('Created user groups: Editors, Users, Admin')

    def create_sample_users(self):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserProfile.objects.get_or_create(user=admin_user)
            admin_user.groups.add(Group.objects.get(name='Admin'))
            self.stdout.write('Created admin user: admin/admin123')

        # Create editor user
        editor_user, created = User.objects.get_or_create(
            username='editor',
            defaults={
                'email': 'editor@example.com',
                'first_name': 'Editor',
                'last_name': 'User'
            }
        )
        if created:
            editor_user.set_password('editor123')
            editor_user.save()
            UserProfile.objects.get_or_create(user=editor_user)
            editor_user.groups.add(Group.objects.get(name='Editors'))
            self.stdout.write('Created editor user: editor/editor123')

        # Create regular user
        regular_user, created = User.objects.get_or_create(
            username='user',
            defaults={
                'email': 'user@example.com',
                'first_name': 'Regular',
                'last_name': 'User'
            }
        )
        if created:
            regular_user.set_password('user123')
            regular_user.save()
            UserProfile.objects.get_or_create(user=regular_user)
            regular_user.groups.add(Group.objects.get(name='Users'))
            self.stdout.write('Created regular user: user/user123')

    def create_sample_tags(self):
        tags_data = [
            'Technology',
            'Programming',
            'Django',
            'Python',
            'Web Development',
            'Tutorial',
            'News',
            'Tips'
        ]
        
        for tag_name in tags_data:
            Tag.objects.get_or_create(name=tag_name)
        
        self.stdout.write(f'Created {len(tags_data)} sample tags')

    def create_sample_articles(self):
        editor_profile = UserProfile.objects.get(user__username='editor')
        
        articles_data = [
            {
                'title': 'Getting Started with Django REST Framework',
                'text': 'Django REST Framework is a powerful and flexible toolkit for building Web APIs. In this article, we will explore the basics of creating RESTful APIs using Django REST Framework.',
                'tags': ['Django', 'Python', 'Web Development', 'Tutorial']
            },
            {
                'title': 'Advanced Python Programming Techniques',
                'text': 'Python is a versatile programming language with many advanced features. This article covers decorators, generators, context managers, and other advanced Python concepts.',
                'tags': ['Python', 'Programming', 'Tutorial', 'Tips']
            },
            {
                'title': 'Building Modern Web Applications',
                'text': 'Modern web applications require careful consideration of architecture, performance, and user experience. Learn about the latest trends and best practices in web development.',
                'tags': ['Web Development', 'Technology', 'Tips']
            }
        ]
        
        for article_data in articles_data:
            tags = article_data.pop('tags')
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'author': editor_profile,
                    'text': article_data['text'],
                    'status': 'published'
                }
            )
            if created:
                # Add tags to the article
                for tag_name in tags:
                    tag = Tag.objects.get(name=tag_name)
                    article.tags.add(tag)
        
        self.stdout.write(f'Created {len(articles_data)} sample articles')

    def create_sample_comments(self):
        articles = Article.objects.all()
        user_profile = UserProfile.objects.get(user__username='user')
        
        comments_data = [
            'Great article! Very helpful for beginners.',
            'Thanks for sharing this tutorial.',
            'I learned a lot from this post.',
            'Could you write more about this topic?',
            'Excellent explanation!',
            'This helped me solve my problem.'
        ]
        
        comment_count = 0
        for article in articles:
            for i, comment_text in enumerate(comments_data[:2]):  # 2 comments per article
                Comment.objects.get_or_create(
                    article=article,
                    author=user_profile,
                    text=comment_text
                )
                comment_count += 1
        
        self.stdout.write(f'Created {comment_count} sample comments')



from django.db import migrations

def create_initial_data(apps, schema_editor):

    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('api', 'UserProfile')
    Article = apps.get_model('api', 'Article')
    Comment = apps.get_model('api', 'Comment')

    user1 = User.objects.create_user(username='user1', password='password123', email='user1@example.com')
    user2 = User.objects.create_user(username='user2', password='password123', email='user2@example.com')

    profile1 = UserProfile.objects.create(user=user1, bio='Bio for user 1')
    profile2 = UserProfile.objects.create(user=user2, bio='Bio for user 2')
    
    article1 = Article.objects.create(
        author=profile1, 
        title='First Article Title', 
        text='This is the content of the first article.',
        status='published'
    )
    article2 = Article.objects.create(
        author=profile2, 
        title='Second Article by Another Author', 
        text='Content for the second article goes here.',
        status='published'
    )

    Comment.objects.create(author=profile2, article=article1, text='Great first article!')
    Comment.objects.create(author=profile1, article=article1, text='Thank you!')
    
    Comment.objects.create(author=profile1, article=article2, text='Interesting perspective.')
    Comment.objects.create(author=profile2, article=article2, text='Glad you think so.')


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_post_comment_article_rename_post_article_and_more'),  
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
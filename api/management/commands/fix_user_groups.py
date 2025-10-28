from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Fix user groups - add all users to Users group'

    def handle(self, *args, **options):
        # Get or create Users group
        users_group, created = Group.objects.get_or_create(name='Users')
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created Users group'))
        else:
            self.stdout.write(self.style.SUCCESS('Users group already exists'))
        
        # Add all users to Users group
        users = User.objects.all()
        added_count = 0
        
        for user in users:
            if not user.groups.filter(name='Users').exists():
                user.groups.add(users_group)
                added_count += 1
                self.stdout.write(f'Added user {user.username} to Users group')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {added_count} users to Users group')
        )

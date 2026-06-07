"""Create demo accounts if they don't already exist."""
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Create demo accounts (admin + demo) if they do not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', email='', password='admin123')
            self.stdout.write(self.style.SUCCESS('✓ Admin account created (admin / admin123)'))
        else:
            self.stdout.write('  - Admin account already exists')

        if not User.objects.filter(username='demo').exists():
            User.objects.create_user('demo', password='demo123')
            self.stdout.write(self.style.SUCCESS('✓ Demo account created (demo / demo123)'))
        else:
            self.stdout.write('  - Demo account already exists')

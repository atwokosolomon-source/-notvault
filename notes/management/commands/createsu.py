# notes/management/commands/createsu.py
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Creates a superuser automatically'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SU_NAME', 'admin')
        email    = os.environ.get('DJANGO_SU_EMAIL', 'admin@notvault.com')
        password = os.environ.get('DJANGO_SU_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write('✅ Superuser created successfully!')
        else:
            self.stdout.write('⚠️ Superuser already exists — skipping.')
import os
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Создайте суперпользователя, если его ещё нет'

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME')
        first_name = os.getenv('ADMIN_FIRSTNAME')
        last_name = os.getenv('ADMIN_LASTNAME')
        email = os.getenv('ADMIN_EMAIL')
        password = os.getenv('ADMIN_PASSWORD')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Суперпользователь "{username}" уже существует'))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            self.stdout.write(self.style.SUCCESS(f'Суперпользователь "{username}" успешно создан'))

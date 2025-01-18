from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument('username', help="Admin's username")
        parser.add_argument('email', help="Admin's email")
        parser.add_argument('password', help="Admin's password")
        parser.add_argument('first_name', help="Admin's first name")
        parser.add_argument('last_name', help="Admin's last name")

    def handle(self, *args, **options):
        if not User.objects.filter(email=options['email']).exists():
            User.objects.create_superuser(
                username=options['username'],
                email=options['email'],
                password=options['password'],
                first_name=options['first_name'],
                last_name=options['last_name'],
            )
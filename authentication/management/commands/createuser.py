from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.core.validators import validate_email

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a new regular user interactively'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Create a regular user"))

        try:
            first_name = self.get_input('First Name')
            last_name = self.get_input('Last Name')
            email = self.get_input('Email')
            password = self.get_password()

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'User created successfully: {email}'))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {str(e)}'))

    def get_input(self, field_name):
        while True:
            value = input(f"{capfirst(field_name)}: ")
            if field_name.lower() == 'email':
                try:
                    validate_email(value)
                    return value
                except ValidationError:
                    self.stdout.write(self.style.ERROR("Invalid email. Please try again."))
            elif value:
                return value
            else:
                self.stdout.write(self.style.ERROR(f"{field_name} cannot be empty."))

    def get_password(self):
        while True:
            password = input("Password: ")
            password_confirm = input("Confirm Password: ")
            if password == password_confirm:
                return password
            self.stdout.write(self.style.ERROR("Passwords do not match. Please try again."))

import validators
from .user_repository import UserRepository
from django.contrib.auth.hashers import make_password, check_password
from .validation_service import ValidationService

class UserService():
    def __init__(self, user_repo=None, validator=None):
        self.user_repo = user_repo or UserRepository() 
        self.validator = validator or ValidationService()
    
    @staticmethod
    def _hash_password(password):
        """Wraps around the django-provided function to hash a password."""
        return make_password(password)

    def create_account(self, email, password):
        """Function for creating an account with a hashed password. It also cheks if the provided email is formatted properly."""
        hashed = UserService._hash_password(password)
        return self.user_repo.create_user(email, hashed)
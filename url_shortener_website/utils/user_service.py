import validators
from .user_repository import UserRepository
from django.contrib.auth.hashers import make_password, check_password

class UserService():
    # TESTED
    def is_email_valid(email):
        return validators.email(email)
    
    # TESTED 
    def hash_password(password):
        return make_password(password)

    # TESTED
    def create_account(email, password):
        hashed = UserService.hash_password(password)
        return UserRepository().create_user(email, hashed)
    
    # TESTED
    def is_password_valid(user, password):
        return check_password(password, user.hashed_password)
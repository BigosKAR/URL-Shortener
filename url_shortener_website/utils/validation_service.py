import validators
import validators
from django.contrib.auth.hashers import check_password


class ValidationService():
    @staticmethod
    def is_url_valid(url):
        result =  validators.url(url)
        if not result:
            return False
        print("Validation passed. Moving on to DB entry creation.")
        return True
    
    @staticmethod    
    def is_password_valid(user, password):
        """Checks if the password provided is equal to the actual hashed password"""
        if user is None:
            return False
        return check_password(password, user.hashed_password)
    
    @staticmethod
    def is_email_valid(email):
        """Returns True/False depending on the validity of the provided email."""
        return validators.email(email)
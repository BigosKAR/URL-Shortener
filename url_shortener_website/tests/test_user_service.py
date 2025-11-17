from django.test import TestCase, SimpleTestCase
from url_shortener_website.utils.user_service import UserService
from url_shortener_website.utils.user_repository import UserRepository
from ..models import UserAccount

# Create your tests here.

class TestUserServiceIntegration(TestCase):
    def test_create_account(self):
        user = UserService.create_account("test_email@gmail.com", "test")
        self.assertEqual(user.email, "test_email@gmail.com")
        self.assertNotEqual(user.hashed_password, "mypassword")
        self.assertTrue(user.hashed_password.startswith("pbkdf2_")) # Django uses this prefix
        self.assertTrue(UserRepository.email_taken("test_email@gmail.com"))

class TestUserServiceUnit(TestCase):
    def test_is_email_valid(self):
        valid = UserService.is_email_valid("valid@gmail.com")
        self.assertTrue(valid, True)

    def test_is_email_invalid(self):
        invalid = UserService.is_email_valid("invalid")
        self.assertFalse(invalid, False)

    def test_hash_password(self):
        password = "test"
        hashed = UserService.hash_password(password)
        self.assertNotEqual(hashed, password)
        self.assertTrue(hashed.startswith("pbkdf2_"))  # Django uses this prefix

    def test_is_password_valid_true(self):
        user = UserService.create_account("test_email@gmail.com", "test")
        self.assertTrue(UserService.is_password_valid(user, "test"))

    def test_is_password_valid_false(self):
        user = UserService.create_account("test_email@gmail.com", "test")
        self.assertFalse(UserService.is_password_valid(user, "random-password"))

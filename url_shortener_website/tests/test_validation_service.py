from django.test import SimpleTestCase
from url_shortener_website.utils.user_service import UserService
from url_shortener_website.utils.validation_service import ValidationService
from unittest.mock import Mock

class TestUserServiceUnit(SimpleTestCase):
    def setUp(self):
        self.mock_repo = Mock()
        self.validation = ValidationService()
        self.user_service = UserService()

    def test_is_email_valid(self):
        self.assertTrue(self.validation.is_email_valid("valid@gmail.com"))

    def test_is_email_invalid(self):
        self.assertFalse(self.validation.is_email_valid("invalid"))

    def test_is_password_valid_true(self):
        mock_user = Mock()
        mock_user.hashed_password = self.user_service._hash_password("mypassword")
        self.assertTrue(self.validation.is_password_valid(mock_user, "mypassword"))

    def test_is_password_valid_false(self):
        mock_user = Mock()
        mock_user.hashed_password = self.user_service._hash_password("mypassword")
        self.assertFalse(self.validation.is_password_valid(mock_user, "random-password"))

    def test_is_password_valid_user_none(self):
        self.assertFalse(self.validation.is_password_valid(None, "anything"))
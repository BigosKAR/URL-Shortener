from django.test import TestCase
from url_shortener_website.utils.user_service import UserService
from url_shortener_website.utils.user_repository import UserRepository
# Create your tests here.

class TestUserServiceIntegration(TestCase):
    def setUp(self):
        self.user_repo = UserRepository()
        self.user_service = UserService(user_repo=self.user_repo)

    def test_create_account(self):
        user = self.user_service.create_account("test_email@gmail.com", "test")
        self.assertEqual(user.email, "test_email@gmail.com")
        self.assertTrue(user.hashed_password.startswith("pbkdf2_"))
        self.assertTrue(self.user_repo.email_taken("test_email@gmail.com"))
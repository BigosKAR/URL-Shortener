from django.test import TestCase
from url_shortener_website.utils.user_repository import UserRepository
from ..models import UserAccount

# Create your tests here.

class TestUserRepositoryIntegration(TestCase):
    def setUp(self):
        self.repo = UserRepository()

    def test_get_by_id_exists(self):
        test_user = UserAccount.objects.create(email="test_user@example.com", hashed_password="test")
        fetched = self.repo.get_by_id(test_user.id)
        self.assertEqual(fetched, test_user)

    def test_get_by_id_not_exists(self):
        fetched = self.repo.get_by_email(1)
        self.assertIsNone(fetched)

    def test_get_by_email_exists(self):
        test_user = UserAccount.objects.createcreate(email="test_user@example.com", hashed_password="test")
        fetched = self.repo.get_by_email("test_user@example.com")
        self.assertEqual(fetched, test_user)

    def test_get_by_email_not_exists(self):
        fetched = self.repo.get_by_email("non-existent")
        self.assertIsNone(fetched)

    def test_email_taken(self):
        UserAccount.objects.create(email="test_user@example.com", hashed_password="test")
        taken = self.repo.email_taken("test_user@example.com")
        self.assertEqual(taken, True)
    
    def test_email_not_taken(self):
        taken = self.repo.email_taken("test_user@example.com")
        self.assertEqual(taken, False)

    def test_create_user(self):
        user = self.repo.create_user("new_email@gmail.com", "123")
        self.assertIsInstance(user, UserAccount)
        self.assertEqual(user.email, "new_email@gmail.com")
        self.assertTrue(UserAccount.objects.filter(email="new_email@gmail.com").exists())

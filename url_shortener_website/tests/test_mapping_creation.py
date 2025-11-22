from django.test import TestCase
from url_shortener_website.utils.mapping_creation_service import MappingCreationService
from ..models import UrlMapping, UserUrlMapping, UserAccount


class TestMappingCreationService(TestCase):
    def setUp(self):
        class Session(dict):
            def flush(self):
                self.clear()
        
        class Request:
            def __init__(self):
                self.session = Session()
        
        self.request = Request()
        self.mapping_creator = MappingCreationService(self.request)

    def test_create_mapping_new(self):
        entry, created = self.mapping_creator.create_mapping("https://google.com")

        self.assertTrue(created)
        self.assertEqual(entry.original_url, "https://google.com")
        self.assertTrue(len(entry.shortcode) > 0) # the shortcode has at least 1 character
        self.assertEqual(UrlMapping.objects.count(), 1)

    def test_create_mapping_existing(self):
        self.mapping_creator.create_mapping("https://example1.com")

        entry, created = self.mapping_creator.create_mapping("https://example1.com")

        self.assertFalse(created)
        self.assertEqual(UrlMapping.objects.count(), 1)

    def test_create_mapping_new_with_existing_user(self):
        sample_user = UserAccount.objects.create(
            email="test_user@gmail.com",
            hashed_password="test"
        )

        self.request.session['user_id'] = sample_user.id

        entry, created = self.mapping_creator.create_mapping("https://example1.com")

        self.assertTrue(created)
        self.assertTrue(
            UserUrlMapping.objects.filter(user_id=sample_user.id, url_id=entry.id).exists()
        )

    def test_create_mapping_existing_url_with_existing_user(self):
        entry1, created1 = self.mapping_creator.create_mapping("https://example.com")

        test_user = UserAccount.objects.create(email="test_user@gmail.com", hashed_password="test")
        self.request.session['user_id'] = test_user.id

        entry2, created = self.mapping_creator.create_mapping("https://example.com")

        self.assertFalse(created)
        self.assertEqual(entry1.id, entry2.id)
        # Checking if the users account is not "following" an existing entry
        self.assertTrue(
            UserUrlMapping.objects.filter(user_id=test_user.id, url_id=entry2.id).exists()
        )

    def test_create_mapping_invalid_user_id(self):
        self.request.session['user_id'] = 10021020

        entry, created = self.mapping_creator.create_mapping("https://baduser.com")

        self.assertTrue(created)
        self.assertEqual(UserUrlMapping.objects.count(), 0)
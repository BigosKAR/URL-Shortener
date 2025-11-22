from django.test import TestCase, SimpleTestCase
from url_shortener_website.utils.url_service import URLService
from ..models import UrlMapping, UserUrlMapping, UserAccount
from unittest.mock import patch, MagicMock, Mock


# Create your tests here.

# Unit tests

class TestUrlServiceUnit(TestCase):
    def setUp(self):
        class Session(dict):
            def flush(self):
                self.clear()
        
        class Request:
            def __init__(self):
                self.session = Session()

        self.request = Request()
        self.url_service = URLService(request=self.request)

    def test_is_url_valid_success(self):
        sample_url = "https://example.com"

        result = self.url_service.is_url_valid(sample_url)

        self.assertEqual(result, True)

    def test_is_url_valid_fail(self):
        sample_url = "https:example.com"

        result = self.url_service.is_url_valid(sample_url)

        self.assertEqual(result, False)

    def test_is_url_valid_success(self):
        sample_url = "https://example.com"

        result = self.url_service.is_url_valid(sample_url)

        self.assertEqual(result, True)

    @patch("url_shortener_website.utils.url_repository.UrlRepository.get_latest")
    def test_get_latest(self, mock_get_latest):
        mock_url1 = Mock()
        mock_url1.shortcode = "def"
        mock_url1.original_url = "https://example2.com"

        mock_url2 = Mock()
        mock_url2.shortcode = "abc"
        mock_url2.original_url = "https://example1.com"
        mock_get_latest.return_value = [
            mock_url1,
            mock_url2,
        ]

        result = self.url_service.get_latest(2)

        self.assertEqual(result, {
            "http://127.0.0.1:8000/def": "https://example2.com",
            "http://127.0.0.1:8000/abc": "https://example1.com"
        })

    @patch("url_shortener_website.utils.user_url_mapping_repository.UserUrlRepository.get_user_mappings")
    @patch("url_shortener_website.utils.url_repository.UrlRepository.get_multiple_by_id")
    def test_get_user_urls(self, mock_get_user_mappings, mock_get_mapping_urls):
        mock_get_user_mappings.return_value = [MagicMock(shortcode="abc", original_url="https://example1.com", clicks=10)]
    
        result = self.url_service.get_user_urls(1)

        self.assertEqual(result, {
            "abc": {
                "shortened_url": "http://127.0.0.1:8000/abc",
                "original_url": "https://example1.com",
                "clicks": 10
            }
        })

    @patch("url_shortener_website.utils.url_repository.UrlRepository.increment_clicks")
    def test_increment_clicks(self, mock_inc):
        mock_inc.return_value = "https://example.com"

        result = self.url_service.increment_clicks("abc")

        mock_inc.assert_called_once_with("abc")
        self.assertEqual(result, "https://example.com")

# Integration tests

class TestUrlServiceIntegration(TestCase):
    def setUp(self):
        class Session(dict):
            def flush(self):
                self.clear()
        
        class Request:
            def __init__(self):
                self.session = Session()
        
        self.request = Request()
        self.url_service = URLService(request=self.request)

    def test_create_mapping_new(self):
        entry, created = self.url_service.create_mapping("https://google.com")

        self.assertTrue(created)
        self.assertEqual(entry.original_url, "https://google.com")
        self.assertTrue(len(entry.shortcode) > 0) # the shortcode has at least 1 character
        self.assertEqual(UrlMapping.objects.count(), 1)

    def test_create_mapping_existing(self):
        self.url_service.create_mapping("https://example1.com")

        entry, created = self.url_service.create_mapping("https://example1.com")

        self.assertFalse(created)
        self.assertEqual(UrlMapping.objects.count(), 1)

    def test_create_mapping_new_with_existing_user(self):
        sample_user = UserAccount.objects.create(
            email="test_user@gmail.com",
            hashed_password="test"
        )

        self.request.session['user_id'] = sample_user.id

        entry, created = self.url_service.create_mapping("https://example1.com")

        self.assertTrue(created)
        self.assertTrue(
            UserUrlMapping.objects.filter(user_id=sample_user.id, url_id=entry.id).exists()
        )

    def test_create_mapping_existing_url_with_existing_user(self):
        entry1, created1 = self.url_service.create_mapping("https://example.com")

        test_user = UserAccount.objects.create(email="test_user@gmail.com", hashed_password="test")
        self.request.session['user_id'] = test_user.id

        entry2, created = self.url_service.create_mapping("https://example.com")

        self.assertFalse(created)
        self.assertEqual(entry1.id, entry2.id)
        # Checking if the users account is not "following" an existing entry
        self.assertTrue(
            UserUrlMapping.objects.filter(user_id=test_user.id, url_id=entry2.id).exists()
        )

    def test_create_mapping_invalid_user_id(self):
        self.request.session['user_id'] = 10021020

        entry, created = self.url_service.create_mapping("https://baduser.com")

        self.assertTrue(created)
        self.assertEqual(UserUrlMapping.objects.count(), 0)
from django.test import TestCase, SimpleTestCase
from url_shortener_website.utils.session_manager import SessionManager
from url_shortener_website.utils.url_mapping_repository import URLMappingRepository
from url_shortener_website.utils.url_service import URLService
from url_shortener_website.utils.user_repository import UserRepository
from url_shortener_website.utils.user_service import UserService
from url_shortener_website.utils.user_url_mapping_repository import UserUrlRepository

# Create your tests here.

class TestSessionManager(SimpleTestCase):
    def setUp(self):
        class Session(dict):
            def flush(self):
                self.clear()
        
        class Request:
            def __init__(self):
                self.session = Session()
        
        self.request = Request()

    def test_set_session_id(self):
        SessionManager.set_session_id(self.request, user_id=123)
        self.assertEqual(self.request.session.get('user_id'), 123)

    def test_get_session_id(self):
        TEST_ID = 456
        self.request.session['user_id'] = TEST_ID
        user_id = SessionManager.get_session_id(self.request)
        self.assertEqual(user_id, TEST_ID)

    def test_get_session_id_none_if_missing(self):
        user_id = SessionManager.get_session_id(self.request)
        self.assertIsNone(user_id)

    def test_clearing_session(self):
        self.request.session['user_id'] = 789
        SessionManager.clear_session(self.request)
        self.assertNotIn('user_id', self.request.session)
        self.assertEqual(self.request.session, {})
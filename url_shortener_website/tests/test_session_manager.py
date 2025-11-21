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
        
        self.session = Session()
        self.manager = SessionManager(self.session)

    def test_set_session_id(self):
        self.manager.set_user_id(user_id=123)
        self.assertEqual(self.session.get('user_id'), 123)

    def test_get_session_id(self):
        TEST_ID = 456
        self.session['user_id'] = TEST_ID
        user_id = self.manager.get_user_id()
        self.assertEqual(user_id, TEST_ID)

    def test_get_session_id_none_if_missing(self):
        user_id = self.manager.get_user_id()
        self.assertIsNone(user_id)

    def test_clearing_session(self):
        self.session['user_id'] = 789
        self.manager.clear()
        self.assertNotIn('user_id', self.session)
        self.assertEqual(self.session, {})
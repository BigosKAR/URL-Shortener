from django.test import SimpleTestCase
from url_shortener_website.utils.session_manager import SessionManager

# Create your tests here.

class TestSessionManager(SimpleTestCase):
    def setUp(self):
        class Session(dict):
            def flush(self):
                self.clear()
        
        class Request():
            def __init__(self, session):
                self.session = session
        self.request = Request(Session())
        self.manager = SessionManager(self.request)

    def test_set_session_id(self):
        self.manager.set_user_id(user_id=123)
        self.assertEqual(self.request.session.get('user_id'), 123)

    def test_get_session_id(self):
        TEST_ID = 456
        self.request.session['user_id'] = TEST_ID
        user_id = self.manager.get_user_id()
        self.assertEqual(user_id, TEST_ID)

    def test_get_session_id_none_if_missing(self):
        user_id = self.manager.get_user_id()
        self.assertIsNone(user_id)

    def test_clearing_session(self):
        self.request.session['user_id'] = 789
        self.manager.clear()
        self.assertNotIn('user_id', self.request.session)
        self.assertEqual(self.request.session, {})
import base62
from .url_repository import UrlRepository
from .session_manager import SessionManager
from .user_url_mapping_repository import UserUrlRepository
from .user_repository import UserRepository
from .url_fetcher_service import UrlFetcherService
import os

BASE_URL = os.environ.get("WEBSITE_HOSTNAME", '127.0.0.1:8000')
if BASE_URL == '127.0.0.1:8000':
    COMPLETE_URL = 'http://' + BASE_URL
else:
    COMPLETE_URL = 'https://' + BASE_URL

class MappingCreationService():
    def __init__(self, request):
        self.request = request
        self.url_repo = UrlRepository()
        self.user_repo = UserRepository()
        self.user_url_repo = UserUrlRepository(
            user_repo=self.user_repo,
            url_repo=self.url_repo
        )
        self.url_fetcher = UrlFetcherService(
            url_repo=self.url_repo,
            user_url_repo=self.user_url_repo
        )

    @staticmethod
    def _create_shortcode(entry_id):
        """Function creates a shortcode by encoding its ID with base62"""
        return base62.encode(entry_id)

    def create_mapping(self, original_url):
        """Creates all the necessary entries given the provided details."""
        entry, created = self.url_repo.get_or_create(original_url)
        if entry is None:
            return False
        
        if created:
            entry.shortcode = MappingCreationService._create_shortcode(entry.id)
            entry.save()
            
        supplied_uid = SessionManager(self.request).get_user_id()
        try:
            uid = int(supplied_uid)
        except Exception:
            uid = None

        if uid is not None:
            user = self.user_repo.get_by_id(uid)

            if user is not None:
                self.user_url_repo.create_if_no_entry(uid, entry.id)

        return entry, created
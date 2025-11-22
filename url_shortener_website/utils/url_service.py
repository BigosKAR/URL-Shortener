from ..models import UrlMapping
import base62
from .url_repository import UrlRepository
from .session_manager import SessionManager
from .user_url_mapping_repository import UserUrlRepository
from .user_repository import UserRepository
from .url_fetcher_service import UrlFetcherService
from .validation_service import ValidationService
from .mapping_creation_service import MappingCreationService
import os
import validators

BASE_URL = os.environ.get("WEBSITE_HOSTNAME", '127.0.0.1:8000')
if BASE_URL == '127.0.0.1:8000':
    COMPLETE_URL = 'http://' + BASE_URL
else:
    COMPLETE_URL = 'https://' + BASE_URL

class URLService():
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
        self.validator = ValidationService()
        self.mapping_creator = MappingCreationService(self.request) 

    def get_user_urls(self, id):
        """Returns urls which are assigned to the user with this specific ID."""
        return self.url_fetcher.get_user_urls(id)
    
    def get_latest(self, amount):
        """Returns the latest urls in terms of order."""
        return self.url_fetcher.get_latest(amount)
    
    def is_url_valid(self, url):
        """Checks if the provided url is valid."""
        return self.validator.is_url_valid(url)
    
    def create_mapping(self, original_url):
        """Creates a mapping for the provided url. If there is a user logged in, it will connect that entry to the user."""
        return self.mapping_creator.create_mapping(original_url)
    
    def increment_clicks(self, shortcode):
        """Increments clicks for an entry with the provided shortcode."""
        return self.url_repo.increment_clicks(shortcode)
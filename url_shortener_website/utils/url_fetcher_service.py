from ..models import UrlMapping
import base62
from .url_repository import UrlRepository
from .session_manager import SessionManager
from .user_url_mapping_repository import UserUrlRepository
from .user_repository import UserRepository
import os
import validators

BASE_URL = os.environ.get("WEBSITE_HOSTNAME", '127.0.0.1:8000')
if BASE_URL == '127.0.0.1:8000':
    COMPLETE_URL = 'http://' + BASE_URL
else:
    COMPLETE_URL = 'https://' + BASE_URL

class UrlFetcherService():
    def __init__(self, url_repo=None, user_url_repo=None):
        self.url_repo = url_repo or UrlRepository()
        self.user_url_repo = user_url_repo or UserUrlRepository(url_repo=self.url_repo)

    def get_user_urls(self, id):
        """Returns a dictionary containing all URL data assigned to the user ID."""
        ids = self.user_url_repo.get_user_mappings(id)
        urls_objs = self.url_repo.get_multiple_by_id(ids)

        result = {}
        for url in urls_objs:
            # url is a model instance; access attributes directly
            result[url.shortcode] = {
                "shortened_url": f"{COMPLETE_URL}/{url.shortcode}",
                "original_url": url.original_url,
                "clicks": getattr(url, 'clicks', 0)
            }
        return result
    
    def get_latest(self, amount):
        """Returns a dictionary containing n amount of latest URL data in terms of when they were added"""
        latest_urls = self.url_repo.get_latest(amount)
        url_json = {}


        for url in latest_urls:
            url_json[f"{COMPLETE_URL}/{url.shortcode}"] = url.original_url

        return url_json # Returns a dictionary containing latest urls
    
 
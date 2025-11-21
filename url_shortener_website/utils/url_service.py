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

class URLService():
    def __init__(self, request):
        self.session = request.session

    @staticmethod
    def get_user_urls(id):
        ids = UserUrlRepository.get_user_mappings(id)
        urls_objs = UrlRepository.get_multiple_by_id(ids)

        result = {}
        for url in urls_objs:
            # url is a model instance; access attributes directly
            result[url.shortcode] = {
                "shortened_url": f"{COMPLETE_URL}/{url.shortcode}",
                "original_url": url.original_url,
                "clicks": getattr(url, 'clicks', 0)
            }
        return result
    
    @staticmethod
    def get_latest(amount):
        latest_urls = UrlRepository().get_latest(amount)
        url_json = {}


        for url in latest_urls.values:
            url_json[f"{COMPLETE_URL}/{url['shortcode']}"] = url['original_url']

        return url_json # Returns a dictionary containing latest urls
    
    @staticmethod
    def is_url_valid(url):
        result =  validators.url(url)
        if not result:
            return False
        print("Validation passed. Moving on to DB entry creation.")
        return True
    
    @staticmethod
    def create_shortcode(entry_id):
        return base62.encode(entry_id)
    
    def create_mapping(self, original_url):
        entry, created = UrlRepository().get_or_create(original_url)
        if entry is None:
            return False
        
        if created:
            # Getting the newly created entry to update the shortcode
            entry.shortcode = URLService.create_shortcode(entry.id)
            entry.save()
            print(f"New Entry ID: {entry.id}")
            print(f"The Base 62 encoded version: {entry.shortcode}") 
            
        supplied_uid = SessionManager(self.session).get_user_id()
        try:
            uid = int(supplied_uid)
        except Exception:
            print(f"Invalid user id provided: {supplied_uid}")
            uid = None

        if uid is not None:
            user = UserRepository.get_by_id(uid)

            if user is not None:
                UserUrlRepository.create_if_no_entry(uid, entry.id)

        return entry, created
    
    @staticmethod
    def increment_clicks(shortcode):
        return UrlRepository.increment_clicks(shortcode)
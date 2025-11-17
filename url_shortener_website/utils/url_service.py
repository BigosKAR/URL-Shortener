from ..models import UrlMapping
import validators
import base62
from .url_mapping_repository import URLMappingRepository
from .session_manager import SessionManager
from .user_url_mapping_repository import UserUrlRepository
from .user_repository import UserRepository

BASE_URL = 'http://127.0.0.1:8000'

class URLService():
    def __init__(self, request):
        self.request = request

    # TESTED
    def get_user_urls(id):
        mappings = UserUrlRepository.get_user_mappings(id)
        urls = URLMappingRepository.get_mapping_urls(mappings)

        result = {}
        for url in urls:
            # url is a model instance; access attributes directly
            result[url.shortcode] = {
                "shortened_url": f"{BASE_URL}/{url.shortcode}",
                "original_url": url.original_url,
                "clicks": getattr(url, 'clicks', 0)
            }
        return result
    
    # TESTED: UNIT ONLY
    def get_latest(amount):
        latest_urls = URLMappingRepository.get_latest_urls(amount)
        url_json = {}

        for url in latest_urls:
            url_json[url['shortcode']] = url['original_url']

        return url_json # Returns a dictionary containing latest urls
    
    # TESTED: SUCCESS/FAIL
    def is_url_valid(url):
        result =  validators.url(url)
        if not result:
            return False
        print("Validation passed. Moving on to DB entry creation.")
        return True
    
    # TESTED
    def create_shortcode(entry_id):
        return base62.encode(entry_id)
    
    # TESTED
    def create_mapping(self, original_url):
        try:
            entry, created = UrlMapping.objects.get_or_create(
                original_url=original_url
            )
        except UrlMapping.MultipleObjectsReturned:
            print("Multiple objects found for the url!")
            return False

        if created:
            # Getting the newly created entry to update the shortcode
            entry.shortcode = URLService.create_shortcode(entry.id)
            entry.save()
            print(f"New Entry ID: {entry.id}")
            print(f"The Base 62 encoded version: {entry.shortcode}") 
            
        supplied_uid = SessionManager.get_session_id(self.request)
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
    
    # TESTED
    def increment_click_count(shortcode):
        return URLMappingRepository.increment_click_count(shortcode)
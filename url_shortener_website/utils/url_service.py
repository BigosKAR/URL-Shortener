from ..models import UrlMapping, UserUrlMapping
from ..api.views import BASE_URL
import validators
import base62
from utils.url_mapping_repo import URLMappingRepository

class URLService():
    def get_user_urls(id):
        urls = URLMappingRepository.get_user_urls(id)

        result = {}
        for url in urls:
            # url is a model instance; access attributes directly
            result[url.shortcode] = {
                "shortened_url": f"{BASE_URL}/{url.shortcode}",
                "original_url": url.original_url,
                "clicks": getattr(url, 'clicks', 0)
            }
        return result
    
    def get_latest(amount):
        latest_urls = URLMappingRepository.get_latest_urls(amount)
        url_json = {}

        for url in latest_urls:
            url_json[url['shortcode']] = url['original_url']

        return url_json # Returns a dictionary containing latest urls
    
    def is_url_valid(url):
        result =  validators.url(url)
        if not result:
            return False
        print("Validation passed. Moving on to DB entry creation.")
        return True
    
    def create_shortcode(entry_id):
        return base62.encode(entry_id)
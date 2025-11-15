from .models import UrlMapping, UserUrlMapping
from .api.views import BASE_URL
    
class UrlFetcher():
    def get_info(self, id):
        mappings = UserUrlMapping.objects.filter(user_id=id).values_list('url_id', flat=True)
        urls = UrlMapping.objects.filter(id__in=list(mappings))

        result = {}
        for url in urls:
            # url is a model instance; access attributes directly
            result[url.shortcode] = {
                "shortened_url": f"{BASE_URL}/{url.shortcode}",
                "original_url": url.original_url,
                "clicks": getattr(url, 'clicks', 0)
            }
        return result
    
    def get_latest(self, amount):
        latest_urls = UrlMapping.objects.order_by("-id").values()[:amount]
        url_json = {}

        for url in latest_urls:
            url_json[url['shortcode']] = url['original_url']

        return url_json # Returns a dictionary containing latest urls
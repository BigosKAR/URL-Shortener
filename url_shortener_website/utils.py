from .models import UrlMapping

class LatestUrlFactory():
    def __init__(self, latest_url_amount):
        self.latest_url_amount = latest_url_amount

    def fetch_urls(self):
        latest_urls = UrlMapping.objects.order_by("-id").values()[:self.latest_url_amount]
        url_json = {}

        for url in latest_urls:
            url_json[url['shortcode']] = url['original_url']

        return url_json # Returns a dictionary containing latest urls
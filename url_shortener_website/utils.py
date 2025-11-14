from .models import UrlMapping

class LatestUrls():
    def get(self, amount):
        latest_urls = UrlMapping.objects.order_by("-id").values()[:amount]
        url_json = {}

        for url in latest_urls:
            url_json[url['shortcode']] = url['original_url']

        return url_json # Returns a dictionary containing latest urls
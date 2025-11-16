from ..models import UrlMapping

# ONLY this class should manipulate the UrlMapping table!
class URLMappingRepository():
    def get_mapping_urls(mappings):
        return UrlMapping.objects.filter(id__in=list(mappings))

    def get_latest_urls(amount):
        return UrlMapping.objects.order_by("-id").values()[:amount]
    
    def increment_click_count(shortcode):
        try:
            url_mapping_object = UrlMapping.objects.get(shortcode=shortcode)
        except UrlMapping.DoesNotExist:
            return None
        
        # Updating clicks
        url_mapping_object.clicks += 1
        url_mapping_object.save()
        return url_mapping_object.original_url
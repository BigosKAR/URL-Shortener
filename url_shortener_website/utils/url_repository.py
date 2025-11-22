from ..models import UrlMapping

# ONLY this class should manipulate the UrlMapping table!
class UrlRepository():
    def __init__(self):
        self.model_cls = UrlMapping 

    def get_multiple_by_id(self, ids):
        """Gets url objects based on the set of entry id's provided."""
        return self.model_cls.objects.filter(id__in=ids)

    def get_latest(self, amount: int):
        """Gets n number of most recent url entries."""
        return self.model_cls.objects.order_by("-id")[:amount]
    
    def increment_clicks(self, shortcode: str):
        url_obj = self._get_by_shortcode(shortcode)
        if not url_obj:
            return None
        
        url_obj.clicks += 1
        url_obj.save()

        return url_obj
    
    def _get_by_shortcode(self, shortcode: str):
        """Private functions for fetching a url object from a shortcode"""
        try:
            url_obj = self.model_cls.objects.get(shortcode=shortcode)
        except self.model_cls.DoesNotExist:
            return None
        
        return url_obj

    def get_or_create(self, url: str):
        """Gets or creates an entry with the provided url."""
        try:
            entry, created = self.model_cls.objects.get_or_create(
                original_url=url
            )
        except UrlMapping.MultipleObjectsReturned:
            print("Multiple objects found for the url!")
            return None, False
        
        return entry, created
    
    def get_by_id(self, id: int):
        """Gets url objects based on the provide url."""
        try:
            url_obj = self.model_cls.objects.get(id=id)
        except self.model_cls.DoesNotExist:
            return False
        
        return url_obj
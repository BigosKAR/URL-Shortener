from ..models import UrlMapping, UserUrlMapping
from ..api.views import BASE_URL
import validators
from url_service import URLService
from user_repository import UserRepository
from user_url_mapping_repository import UserUrlRepository
from session_manager import SessionManager

# ONLY this class should manipulate the UrlMapping table!
class URLMappingRepository():
    def __init__(self, request):
        self.SessionManager = SessionManager(request=request)
    def get_or_create(self, original_url):
        try:
            entry, created = UrlMapping.objects.get_or_create(
                original_url=original_url
            )
        except UrlMapping.MultipleObjectsReturned:
            print("Multiple objects found for the given shortcode and url!")
            return False

        if created:
            # Getting the newly created entry to update the shortcode
            entry.shortcode = URLService.create_shortcode(entry.id)
            entry.save()
            
            supplied_uid = self.SessionManager.get_session_id(self.request)
            try:
                uid = int(supplied_uid)
            except Exception:
                print(f"Invalid user id provided: {supplied_uid}")
                uid = None

            if uid is not None:
                user = UserRepository.get_by_id(uid)

                if user is not None:
                    UserUrlRepository.create_if_no_entry(uid, entry.id)
            print(f"New Entry ID: {entry.id}")
            print(f"The Base 62 encoded version: {entry.shortcode}") 

        return entry, created

    def get_user_urls(user_id):
        mappings = UserUrlRepository.get_user_mappings(user_id)
        return UrlMapping.objects.filter(id__in=list(mappings))

    def get_latest_urls(amount):
        return UrlMapping.objects.order_by("-id").values()[:amount]
    
    def increment_click_count(shortcode):
        try:
            url_mapping_object = UrlMapping.objects.get(shortcode=shortcode)
        except UrlMapping.DoesNotExist:
            return False
        finally:
            # Updating clicks
            url_mapping_object.clicks += 1
            url_mapping_object.save()
        return url_mapping_object.original_url
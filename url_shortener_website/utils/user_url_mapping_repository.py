from ..models import UserUrlMapping, UserAccount, UrlMapping
from user_repository import UserRepository
from url_repository import UrlRepository

# ONLY this class should manipulate the UserUrlMapping table!
class UserUrlRepository():
    def __init__(self, user_repo=None, url_repo=None):
        self.model_cls = UserUrlMapping
        self.user_repo = user_repo
        self.url_repo = url_repo
    
    def _entry_exists(self, user_id: int, url_id: int) -> bool:
        """Returns boolean indicating if an entry with the user and url id exists."""
        return self.model_cls.objects.filter(user_id=user_id, url_id=url_id).exists()

    def _create_entry(self, user_id: int, url_id: int) -> bool:
        """Creates an entry with the given id's"""
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            return False

        url = self.url_repo.get_by_id(url_id)
        if url is None:
            return False

        try:
            self.model_cls.objects.create(user_id=user, url_id=url)
        except Exception as e:
            return False
        return True
    
    def create_if_no_entry(self, user_id: int, url_id: int) -> bool:
        """Creates an entry if it does not exists, otherwise it returns False"""
        if not self._entry_exists(user_id, url_id):
            return self._create_entry(user_id, url_id)
        else:
            return False

    def get_user_mappings(self, user_id: int)-> bool:
        """Returns entries for a specific user using their id."""
        return self.model_cls.objects.filter(user_id=user_id).values_list('url_id', flat=True)

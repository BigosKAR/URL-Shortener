from ..models import UserUrlMapping, UserAccount, UrlMapping

# ONLY this class should manipulate the UserUrlMapping table!
class UserUrlRepository():
    def entry_exists(user_id, url_id):
        exists = UserUrlMapping.objects.filter(user_id=user_id, url_id=url_id).exists()
        return exists

    def create_entry(user_id, url_id):
        # Resolve integer IDs to model instances before assigning to FK fields
        try:
            user = UserAccount.objects.get(id=user_id)
        except UserAccount.DoesNotExist:
            print(f"Cannot create mapping: UserAccount with id={user_id} does not exist.")
            return False

        try:
            url = UrlMapping.objects.get(id=url_id)
        except UrlMapping.DoesNotExist:
            print(f"Cannot create mapping: UrlMapping with id={url_id} does not exist.")
            return False

        try:
            UserUrlMapping.objects.create(user_id=user, url_id=url)
            print("Created a mapping of the URL to the current user.")
        except Exception as e:
            print(f"Unexpected error creating UserUrlMapping: {e}")
            return False
        return True
    
    def create_if_no_entry(user_id, url_id):
        if not UserUrlRepository.entry_exists(user_id, url_id):
            UserUrlRepository.create_entry(user_id, url_id)
        else:
            print("UserUrlMapping already exists; skipping creation.")

    def get_user_mappings(user_id):
        return UserUrlMapping.objects.filter(user_id=user_id).values_list('url_id', flat=True)

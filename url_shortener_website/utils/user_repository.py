from ..models import UserAccount

# ONLY this class should manipulate the UserAccount table!
class UserRepository():
    def __init__(self):
        self.model_cls = UserAccount

    def get_by_id(self, id: int) -> UserAccount | None:
        """Fetches account object by ID and returns if found, otherwise None"""
        try:
            user = self.model_cls.objects.get(id=id)
        except self.model_cls.DoesNotExist:
            user = None
        return user
    
    def get_by_email(self, email: str) -> UserAccount | None:
        """Fetches account object by unique email and returns if found, otherwise None"""
        try:
            account = self.model_cls.objects.get(email=email)
        except self.model_cls.DoesNotExist:
            account = None
        return account
    
    def email_taken(self, email: str) -> bool:
        """Checks if an email is already taken by another entry. Returns True/False"""
        return self.model_cls.objects.filter(email=email).exists()

    def create_user(self, email: str, password: str) -> UserAccount:
        """Creates a new account with the given credentials."""
        account = self.model_cls(email=email, hashed_password=password)
        account.save()
        return account

from ..models import UserAccount

# ONLY this class should manipulate the UserAccount table!
class UserRepository():
    def __init__(self):
        self.cls_model = UserAccount

    def get_by_id(self, id: int) -> UserAccount | None:
        """Fetches account object by ID and returns if found, otherwise None"""
        try:
            user = self.cls_model.objects.get(id=id)
        except self.cls_model.DoesNotExist:
            user = None
        return user
    
    def get_by_email(self, email: str) -> UserAccount | None:
        """Fetches account object by unique email and returns if found, otherwise None"""
        try:
            account = self.cls_model.objects.get(email=email)
        except self.cls_model.DoesNotExist:
            account = None
        return account
    
    def email_taken(self, email: str) -> bool:
        """Checks if an email is already taken by another entry. Returns True/False"""
        return self.cls_model.objects.filter(email=email).exists()

    def create_user(self, email: str, password: str) -> UserAccount:
        """Creates a new account with the given credentials."""
        account = self.cls_model(email=email, hashed_password=password)
        account.save()
        return account

from ..models import UserAccount

# ONLY this class should manipulate the UserAccount table!
class UserRepository():
    # TESTED
    def get_by_id(id):
        try:
            user = UserAccount.objects.get(id=id)
        except UserAccount.DoesNotExist:
            print(f"No UserAccount found for id {id}")
            user = None
        return user
    
    # TESTED
    def get_by_email(email):
        try:
            account = UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            print(f"No UserAccount found for email:")
            account = None
        return account
    
    # TESTED
    def email_taken(email):
        return UserAccount.objects.filter(email=email).exists()

    # TESTED
    def create_user(email, password):
        account = UserAccount(email=email, hashed_password=password)
        account.save()
        return account

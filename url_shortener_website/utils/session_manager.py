from django.http import HttpRequest
from typing import Optional

class SessionManager():
    def __init__(self, request: HttpRequest):
        self.session = request.session

    def set_user_id(self, user_id: int) -> None:
        """Sets the user id in the current session for verification logic."""
        self.session['user_id'] = user_id

    def get_user_id(self) -> Optional[int]:
        """Gets user id saved in session if it exists, returns None otherwise"""
        return self.session.get('user_id')
    
    def clear(self) -> None:
        """Clears the user id from the session"""
        self.session.flush()
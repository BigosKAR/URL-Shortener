class SessionManager():
    def __init__(self, request):
        self.session = request.session

    def set_user_id(self, user_id):
        self.session['user_id'] = user_id

    def get_user_id(self):
        return self.session.get('user_id')
    
    def clear(self):
        self.session.flush()
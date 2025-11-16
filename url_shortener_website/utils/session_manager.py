class SessionManager():
    def set_session_id(request, user_id):
        request.session.set('user_id') = user_id

    def get_session_id(request):
        return request.session.get('user_id')
    
    def clear_session(request):
        request.session.flush()
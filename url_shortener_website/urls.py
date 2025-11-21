from django.urls import path, include

from .views import *
from .api.views import *

urlpatterns = [
    path('', url_shortener_view),
    path('metrics/', metrics),
    path('health/', include('health_check.urls')),
    path('user/dashboard', dashboard_view),
    path('<shortcode>/', redirect_view),
    path('api/generate_shortcode', generate_shortcode),
    path('api/signup', create_account),
    path('api/login', login_account),
    path('api/logout', logout_account),
    path('api/verify_session', verify_session),
]
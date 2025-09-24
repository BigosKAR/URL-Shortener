from django.urls import path

from .views import *

urlpatterns = [
    path('', url_shortener_view),
    path('<shortcode>/', redirect_view),
    path('api/generate_shortcode', generate_shortcode)
    # ... more URL patterns here
]
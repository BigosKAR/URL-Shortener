from django.urls import path

from .views import *

urlpatterns = [
    path('', url_shortener_view),
    path('<int:shortcode>/', redirect_view)
    # ... more URL patterns here
]
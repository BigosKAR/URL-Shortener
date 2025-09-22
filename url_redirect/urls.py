from django.urls import path

from .views import redirect_view

urlpatterns = [
    path('<int:shortcode>/', redirect_view)
    # ... more URL patterns here
]
from django.shortcuts import render, redirect

# Create your views here.
def redirect_view(request, shortcode):
    # Add database logic that will retrieve original URL and redirect there
    return redirect("http://google.com")
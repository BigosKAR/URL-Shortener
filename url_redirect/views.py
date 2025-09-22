from django.shortcuts import render, redirect
from .models import UrlMapping

def url_shortener_view(request, shortcode=None):
    context = {}

    if shortcode is not None:
        context['shortcode'] = shortcode
        print("SHORTCODE FOUND!")
    return render('./templates/main_page.html', template_name="main_page.html", context=context)

# Create your views here.
def redirect_view(request, shortcode):
    # Add database logic that will retrieve original URL and redirect there
    try:
        url_mapping_object = UrlMapping.objects.get(shortcode=shortcode)
    except UrlMapping.DoesNotExist:
        print("No record found! Returning to the main page.")
        return redirect("/", shortcode=shortcode)


    original_url = url_mapping_object.original_url
    print(f"[{shortcode}] - Redirecting to the following website: {original_url}")
    return redirect(original_url)
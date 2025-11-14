from django.shortcuts import render, redirect
from .models import UrlMapping
from django.contrib import messages # Only one message should be in the storage at all times!
from .utils import LatestUrlFactory

DEFAULT_SHORTCODE = '.' # some character that does not collide with the base 62 output

# Views related to the website itself

def url_shortener_view(request):
    context = {}
    saved_messages = messages.get_messages(request)

    if len(saved_messages) != 0:
        # Messages need to be iterated because you are unable to access individual messages. Remember only one message should be in the storage at all times!
        for message in saved_messages:
            if message == "favicon.ico":
                continue # Edge case because the browser tries to access the icon
            print(f"{len(saved_messages)}: {message}")
            context['shortcode'] = message
        # Storage is cleared after accessing it!
        print("SHORTCODE FOUND!")

    context['latest_urls'] = LatestUrlFactory(latest_url_amount=10).fetch_urls()


    return render('./templates/main_page.html', template_name="main_page.html", context=context)

# Create your views here.
def redirect_view(request, shortcode):
    try:
        url_mapping_object = UrlMapping.objects.get(shortcode=shortcode)
    except UrlMapping.DoesNotExist:
        print("No record found! Returning to the main page.")
        if shortcode != "favicon.ico": 
            messages.error(request, shortcode) # Passing the invalid shortcode to the main page to display an error message
        return redirect("/")


    original_url = url_mapping_object.original_url
    print(f"[{shortcode}] - Redirecting to the following website: {original_url}")
    return redirect(original_url)
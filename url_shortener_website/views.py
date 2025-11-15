from django.shortcuts import render, redirect
from .models import UrlMapping
from django.contrib import messages # Only one message should be in the storage at all times!
from .utils import UrlFetcher

DEFAULT_SHORTCODE = '.' # some character that does not collide with the base 62 output

# Views related to the website itself

def url_shortener_view(request):
    """
    
    This view is responsible for loading the main page of the web app.
    If a shortcode is passed (through FallbackStorage), it means it is an invalid shortcode and will be displayed on the website.

    The latest URLs are also passed to the template to be displayed on the site.

    """
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

    context['latest_urls'] = UrlFetcher().get_latest(amount=10)


    return render('./templates/main_page.html', template_name="main_page.html", context=context)

# Create your views here.
def redirect_view(request, shortcode):
    """
    
    Responsible for redirecting to a specific website based on the shortcode.
    If an invalid shortcode is provided, it will be redirect the user to the main page. (Saves the shortcode in the FallbackStorage)

    """
    try:
        url_mapping_object = UrlMapping.objects.get(shortcode=shortcode)
        # Updating clicks
        url_mapping_object.clicks += 1
        url_mapping_object.save()
    except UrlMapping.DoesNotExist:
        print("No record found! Returning to the main page.")
        if shortcode != "favicon.ico": 
            messages.error(request, shortcode) # Passing the invalid shortcode to the main page to display an error message
        return redirect("/")


    original_url = url_mapping_object.original_url
    print(f"[{shortcode}] - Redirecting to the following website: {original_url}")
    return redirect(original_url)


def dashboard_view(request):
    """
    View designed to look at your own URLs to check statistics like click counters
    """
    user_id = request.session.get('user_id')
    if not user_id:
        print("Unauthorized access to dashboard.")
        return redirect('/')

    context = {}
    context['user_urls'] = UrlFetcher().get_info(user_id)
    return render('./templates/dashboard.html', template_name='dashboard.html', context=context)
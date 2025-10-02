from django.shortcuts import render, redirect
from .models import UrlMapping
from django.contrib import messages # Only one message should be in the storage at all times!
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import base62
import validators
from .utils import LatestUrlFactory

DEFAULT_SHORTCODE = '.' # some character that does not collide with the base 62 output
BASE_URL = 'http://127.0.0.1:8000'

# Views related to the REST API

@api_view(['POST'])
def generate_shortcode(request):
    # url = request.POST.get('url', None)
    body = request.data
    if len(body) == 0:
        return Response({"error": "No URL provided."}, status=status.HTTP_400_BAD_REQUEST)

    url = body['url']

    # Validating the URL
    
    if not validators.url(url):
        return Response({"error": f"Invalid URL has been provided! Try Again."}, status=status.HTTP_400_BAD_REQUEST)
    print("Validation passed. Moving on to DB entry creation.")

    # Adding or Finding an entry
    try:
        entry, created = UrlMapping.objects.get_or_create(
            original_url=url
        )
    except UrlMapping.MultipleObjectsReturned:
        print("Multiple objects found for the given shortcode and url!")
        return Response({"error": "Multiple objects found for the given URL and shortcode!"})

    if created:
        # Getting the newly created entry to update the shortcode
        entry.shortcode = base62.encode(entry.id)
        entry.save()
    else:
        return Response({"success": f"{BASE_URL}/{entry.shortcode}"}, status=status.HTTP_200_OK)

    print(f"New Entry ID: {entry.id}")
    print(f"The Base 62 encoded version: {entry.shortcode}")

    return Response({"success": f"{BASE_URL}/{entry.shortcode}"}, status=status.HTTP_201_CREATED)


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
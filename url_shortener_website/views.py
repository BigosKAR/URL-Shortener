from django.shortcuts import render, redirect
from .models import UrlMapping
from django.contrib import messages # Only one message should be in the storage at all times!
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import base62
import validators
from .utils import LatestUrls

BASE_URL = 'http://127.0.0.1:8000'

# Views related to the REST API

@api_view(['POST'])
def generate_shortcode(request):
    """
    
    This function is responsible for fetching the url from the request body and then generating a short URL.
    After the request body has been fetched, the program checks for the validity of the body.
    It checks if the entry with the URL already exists, and creates it otherwise.
    
    In the case of creating a new entry, the shortcode is generated from encoding the id with base62 encoding.

    """
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

    context['latest_urls'] = LatestUrls().get(amount=10)


    return render('./templates/main_page.html', template_name="main_page.html", context=context)

# Create your views here.
def redirect_view(request, shortcode):
    """
    
    Responsible for redirecting to a specific website based on the shortcode.
    If an invalid shortcode is provided, it will be redirect the user to the main page. (Saves the shortcode in the FallbackStorage)

    """
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
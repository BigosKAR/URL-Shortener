from django.shortcuts import render, redirect
from .models import UrlMapping
from django.contrib import messages # Only one message should be in the storage at all times!
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import base62
import validators

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
    # Check for database entries
    try:
        url_object = UrlMapping.objects.get(original_url=url)
        if url_object is not None:
            print("This URL is already stored in the database.")
            return Response({"success": f"{BASE_URL}/{url_object.shortcode}"}, status=status.HTTP_200_OK)
    except UrlMapping.DoesNotExist:
        print("No entry found for this link! Moving on to URL validation.")

    # Validating the URL
    
    if not validators.url(url):
        return Response({"error": f"Invalid URL has been provided: {url}"}, status=status.HTTP_400_BAD_REQUEST)
    print("Validation passed. Moving on to DB entry creation.")

    print("Creating a new entry for the URL")
    # Adding entry to the database
    UrlMapping.objects.create(shortcode=DEFAULT_SHORTCODE, original_url=url)

    # Getting the newly created entry to update the shortcode
    new_entry = UrlMapping.objects.get(original_url=url)
    new_entry.shortcode = base62.encode(new_entry.id)
    new_entry.save()
    print(f"New Entry ID: {new_entry.id}")
    print(f"The Base 62 encoded version: {new_entry.shortcode}")

    return Response({"success": f"{BASE_URL}/{new_entry.shortcode}"}, status=status.HTTP_201_CREATED)

# Views related to the website itself

def url_shortener_view(request):
    context = {}
    saved_messages = messages.get_messages(request)

    if len(saved_messages) != 0:
        # Messages need to be iterated because you are unable to access individual messages. Remember only one message should be in the storage at all times!
        for message in saved_messages:
            print(f"{len(saved_messages)}: {message}")
            context['shortcode'] = message
        # Storage is cleared after accessing it!
        print("SHORTCODE FOUND!")

    return render('./templates/main_page.html', template_name="main_page.html", context=context)

# Create your views here.
def redirect_view(request, shortcode):
    try:
        url_mapping_object = UrlMapping.objects.get(shortcode=shortcode)
    except UrlMapping.DoesNotExist:
        print("No record found! Returning to the main page.")
        messages.error(request, shortcode) # Passing the invalid shortcode to the main page to display an error message
        return redirect("/")


    original_url = url_mapping_object.original_url
    print(f"[{shortcode}] - Redirecting to the following website: {original_url}")
    return redirect(original_url)
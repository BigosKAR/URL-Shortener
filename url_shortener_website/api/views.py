from django.shortcuts import render, redirect
from ..models import UrlMapping
from django.contrib import messages # Only one message should be in the storage at all times!
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import base62
import validators

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


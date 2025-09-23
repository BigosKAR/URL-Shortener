from django.shortcuts import render, redirect
from .models import UrlMapping
from django.contrib import messages # Only one message should be in the storage at all times!
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base62

# Views related to the REST API

@api_view(['POST'])
def generate_shortcode(request):
    url = request.POST.get('url', None)
    if url is None:
        return Response({"error": "No URL provided."})

    # Add url verification here
    shortcode = base62.encode(url)

    print(shortcode)


    return Response({"message": "Test"})

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
from django.shortcuts import render, redirect
from ..models import UrlMapping, UserAccount, UserUrlMapping
from django.contrib import messages # Only one message should be in the storage at all times!
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import base62
import validators
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError

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
        
        supplied_uid = request.session.get('user_id')
        try:
            uid = int(supplied_uid)
        except Exception:
            print(f"Invalid user id provided: {supplied_uid}")
            uid = None

        if uid is not None:
            try:
                user = UserAccount.objects.get(id=uid)
            except UserAccount.DoesNotExist:
                print(f"No UserAccount found for id {uid}")
                user = None

            if user is not None:
                exists = UserUrlMapping.objects.filter(user_id=user, url_id=entry).exists()
                if not exists:
                    try:
                        UserUrlMapping.objects.create(user_id=user, url_id=entry)
                        print("Created a mapping of the URL to the current user.")
                    except IntegrityError as e:
                        print(f"IntegrityError creating UserUrlMapping: {e}")
                    except Exception as e:
                        print(f"Unexpected error creating UserUrlMapping: {e}")
                else:
                    print("UserUrlMapping already exists; skipping creation.")

    else:
        return Response({"success": f"{BASE_URL}/{entry.shortcode}"}, status=status.HTTP_200_OK)

    print(f"New Entry ID: {entry.id}")
    print(f"The Base 62 encoded version: {entry.shortcode}")

    return Response({"success": f"{BASE_URL}/{entry.shortcode}"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def create_account(request):
    
    body = request.data
    if not body:
        return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return Response({"error": "Both 'email' and 'password' are required."}, status=status.HTTP_400_BAD_REQUEST)

    if not validators.email(email):
        return Response({"error": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST)

    if UserAccount.objects.filter(email=email).exists():
        return Response({"error": "Account with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # hash password and create account
    hashed = make_password(password)
    account = UserAccount(email=email, hashed_password=hashed)
    account.save()

    # set session keys so the server recognizes the newly created user as logged in
    try:
        request.session['user_id'] = account.id
        request.session['user_email'] = account.email
    except Exception:
        print("Warning: could not set session for new account")

    return Response({"success": "Account created."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_account(request):
    
    body = request.data
    if not body:
        return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return Response({"error": "Both 'email' and 'password' are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        account = UserAccount.objects.get(email=email)
    except UserAccount.DoesNotExist:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    if not check_password(password, account.hashed_password):
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    # set session keys so the server recognizes logged-in users
    try:
        # DRF Request has a .session attribute when SessionMiddleware is enabled
        request.session['user_id'] = account.id
        request.session['user_email'] = account.email
    except Exception:
        # if session can't be set, continue but warn
        print("Warning: could not set session for login")

    return Response({"success": "Logged in."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_account(request):
    """Log the user out by clearing the session."""
    try:
        request.session.flush()
    except Exception:
        pass
    return Response({"success": "Logged out."}, status=status.HTTP_200_OK)

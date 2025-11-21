from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..utils.url_service import URLService
from ..utils.user_service import UserService
from ..utils.user_repository import UserRepository
from ..utils.session_manager import SessionManager
import os

BASE_URL = os.environ.get("WEBSITE_HOSTNAME", '127.0.0.1:8000')
# Views related to the REST API

@api_view(['POST'])
def generate_shortcode(request):
    # url = request.POST.get('url', None)
    body = request.data
    if len(body) == 0:
        return Response({"error": "No URL provided."}, status=status.HTTP_400_BAD_REQUEST)

    url = body['url']

    # Validating the URL
    if not URLService.is_url_valid(url):
        return Response({"error": f"Invalid URL has been provided! Try Again."}, status=status.HTTP_400_BAD_REQUEST)

    # Adding or Finding an entry    
    entry, created = URLService(request).create_mapping(url)
    if created:
        return Response({"success": f"{entry.shortcode}"}, status=status.HTTP_201_CREATED)
    return Response({"success": f"{entry.shortcode}"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_account(request):
    
    body = request.data
    if not body:
        return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return Response({"error": "Both 'email' and 'password' are required."}, status=status.HTTP_400_BAD_REQUEST)

    if not UserService.is_email_valid(email):
        return Response({"error": "Invalid email address."}, status=status.HTTP_400_BAD_REQUEST)

    if UserRepository.email_taken(email):
        return Response({"error": "Account with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)

    account = UserService.create_account(email, password)

    try:
        SessionManager(request.session).set_user_id(account.id)
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

    account = UserRepository.get_by_email(email)
    if not account:
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    if not UserService.is_password_valid(account, password):
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        SessionManager(request.session).set_user_id(account.id)
    except Exception:
        print("Warning: could not set session for login")

    return Response({"success": "Logged in."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_account(request):
    """Log the user out by clearing the session."""
    try:
        SessionManager(request).clear()
    except Exception:
        print("Could not flush session")
    return Response({"success": "Logged out."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def verify_session(request):
    """
    Verifying session between closing/opening browser. Not relying on local storage.
    """
    user_id = SessionManager(request).get_user_id()
    if not user_id:
        return Response({"error": "unauthorized session"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"success": { "user_id": user_id}}, status=status.HTTP_200_OK)
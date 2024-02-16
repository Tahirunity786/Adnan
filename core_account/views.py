import datetime
import os
import random
import string
from urllib.parse import urlparse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from core_account.renderers import UserRenderer
from rest_framework.views import Response
from rest_framework import status
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token
import requests as efwe
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from requests.exceptions import HTTPError
from django.http import JsonResponse
from rest_framework import generics
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from django.contrib.auth import get_user_model
from core_account.token import get_tokens_for_user
from core_account.utiles import send_otp_email, get_user_by_identifier
from core_account.utiles import generate_otp
from django.contrib.auth import login



User = get_user_model()

from core_account.serializers import (
    CreateUserSerializer,
    SocialSerializer,
   
)




# ======================================= ACCOUNT MANAGEMENT SECTION # ======================================= #
class CreateUserView(APIView):
    """
    Class-based view for creating a new user account.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request for creating a new user.
        """
        serializer = CreateUserSerializer(data=request.data)
        email = request.data.get("email", None)
        mobile = request.data.get('mobile', None)

        if serializer.is_valid():
            account = serializer.save()

            # Send OTP for account verification via email
            if email:
                subject = 'Account Verification: Social Media'
                message = f'Your Account is created, please verify with this OTP {account.otp}. Otp will expire within 5 minutes'
                otp_sent = send_otp_email(account, subject, message)
                if not otp_sent:
                    return Response({"error": "Failed to send OTP email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Process mobile verification if provided
            if mobile:
                pass  # Implement mobile verification logic here

            token = get_tokens_for_user(account)
            response_data = {
                'response': 'Account has been created',
                'username': account.username,
                'email': account.email,
                'id': account.id,
                'token': token
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthAPIView(APIView):
    """
    Google Authentication API View.
    """

    def post(self, request):
        """
        Authenticate user using Google ID token.

        Args:
            request: HTTP request object containing ID token.

        Returns:
            HTTP response with user data and authentication token.
        """
        id_token = request.data.get('idToken')

        try:
            # Verify the ID token
            id_info = verify_oauth2_token(id_token, requests.Request())

            # Get user info
            user_email = id_info.get('email')
            user_image_url = id_info.get('picture')
            name = id_info.get('name')

            if not user_email:
                return Response({"error": "Email not provided in ID token"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user exists in the database, or create a new one
            try:
                user = User.objects.get(email=user_email)
                created = False
            except User.DoesNotExist:
                # Generate a random username and password for new user
                username = user_email.split('@')[0]
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                user = User.objects.create_user(email=user_email, username=username, password=password, full_name=name)
                created = True
            # Download and save the profile picture if available
            if user_image_url:
                try:
                    image_response = efwe.get(user_image_url)
                    image_response.raise_for_status()  # Raise exception for non-200 status codes
                    file_extension = os.path.splitext(urlparse(user_image_url).path)[1] or '.jpg'
                    random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                    file_path = os.path.join(settings.MEDIA_ROOT, random_filename + file_extension)
                    with open(file_path, 'wb') as f:
                        f.write(image_response.content)
                    user.profile.save(random_filename + file_extension, ContentFile(image_response.content), save=True)
                except (requests.RequestException, IOError) as e:
                    return Response({"error": f"Error while fetching image: {e}"}, status=status.HTTP_400_BAD_REQUEST)

            # Generate authentication token
            token = get_tokens_for_user(user)

            # Construct response data
            response_data = {
                'response': 'Account Created' if created else 'Account Logged In',
                'id': user.id,
                'username': user.username,
                'profile_image': user.profile.url if user.profile else None,
                'email': user.email,
                'token': token
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as e:
            # Invalid token
            return Response({"error": f"Invalid token: {e}"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtp(APIView):
    """
    API endpoint to verify OTP (One Time Password) for user authentication.

    This endpoint verifies whether the provided OTP matches the OTP associated
    with the user account and marks the user as verified if the OTP is valid.

    Request Parameters:
        - username: The username or email of the user.
        - otp: The One Time Password to verify.

    Returns:
        - HTTP 202 ACCEPTED if OTP is valid and user is marked as verified.
        - HTTP 400 BAD REQUEST with an error message if:
            - Username or OTP is not provided.
            - User is not found.
            - OTP is invalid or expired.
            - Any other error occurs during processing.

    Permissions:
        - This endpoint allows any user to access it.

    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests to verify OTP for user authentication.

        Args:
            request: HTTP request object containing username and OTP.

        Returns:
            HTTP response indicating the status of OTP verification.

        """
        # Extracting username and OTP from request data
        username = request.data.get('username')
        otp = request.data.get('otp')
        if username and otp:
            try:
                # Check if the provided username is an email or username
                if '@' in username:
                    usr = User.objects.get(email=username)
                else:
                    usr = User.objects.get(username=username)
                  

                # Check if the OTP matches
                if str(usr.otp) == otp:
                    current_time = datetime.datetime.now().time()

                    # Check if OTP delay is within 5 minutes
                    if (current_time.minute - usr.otp_delay.minute) > 5:
                        return Response(
                            status=status.HTTP_400_BAD_REQUEST,
                            data={"message": "Otp Expired"},
                        )

                    # Mark user as verified
                    usr.is_verified = True
                    usr.save()
                    return Response(
                        status=status.HTTP_202_ACCEPTED,
                        data={"message": "Account verified"},
                    )
                else:
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data={"message": "Invalid Otp"},
                    )
            except User.DoesNotExist:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "User not found"},
                )
            except Exception as e:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": f"An error occurred: {str(e)}"},
                )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Username and OTP are required fields"},
            )

class GetNewOtp(APIView):
    """
    API endpoint to generate and send a new OTP (One-Time Password) for account verification via email.
    """
    permission_classes = [AllowAny]  # Allow any user, authenticated or not, to access this endpoint.

    def post(self, request):
        """
        POST method to handle the generation and sending of a new OTP.

        Parameters:
        - request: HTTP request object containing user data.

        Returns:
        - Response: HTTP response indicating the success or failure of the OTP generation and sending process.
        """
        try:
            # Extracting the username or email from the request data
            query = request.data.get('username')
            usr = get_user_by_identifier(query)

            if usr is None:
                # If user is not found, return a 400 Bad Request response with a relevant message
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "User with provided credentials not found"})

            # Checking OTP limit
            if usr.otp_limit is not None and usr.otp_limit >= 30:
                # If OTP limit has been reached or exceeded, return a 400 Bad Request response with a relevant message
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Otp Limit Ended, please try with another email!"})

            # Sending a new OTP for account verification via email
            subject =  'Account Verification: Social Media'
            otp = generate_otp()
            message = f'Your Account is created, please verify with this OTP {otp}. Otp will expire within 5 minutes.'

            # Assign the generated OTP to the user instance
            usr.otp = otp

            # Incrementing OTP limit if it's not None
            if usr.otp_limit is not None:
                usr.otp_limit += 1
            else:
                # If OTP limit is None, initialize it to 1
                usr.otp_limit = 1
            
            usr.save()  # Saving the updated user instance
            send_otp_email(usr, subject, message)  # Send the OTP email to the user

            return Response(status=status.HTTP_200_OK, data={"message": f"Otp sent to {usr.email}"})
        except Exception as e:
            # Catch any exceptions that occur during the process and return a 400 Bad Request response with a generic error message
            print(f"Exception: {str(e)}")
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"An error occurred while processing the request"})



class SocialLoginView(generics.GenericAPIView):
    """Log in using Facebook"""

    serializer_class = SocialSerializer  # Assuming SocialSerializer is defined elsewhere
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data.get('provider')  # Use validated_data instead of data
        access_token = serializer.validated_data.get('access_token')  # Use validated_data instead of data

        strategy = load_strategy(request)

        try:
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if isinstance(backend, BaseOAuth2):
                user = backend.do_auth(access_token)
        except (HTTPError, AuthTokenError, AuthForbidden) as error:
            return Response({'error': 'Invalid credentials', 'details': str(error)}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            # Generate JWT token
            login(request, user)
            token = get_tokens_for_user(user)  # Assuming get_tokens_for_user is defined elsewhere

            # Customize the response
            response_data = {
                'email': user.email,
                'username': user.username,
                'token': token
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({'error': 'Failed to authenticate user'}, status=status.HTTP_400_BAD_REQUEST)



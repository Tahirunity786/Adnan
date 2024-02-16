import random
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# Helper for sending mail for OTP
def send_otp_email(user, subject, message):
    try:
        """
        Helper function to send OTP via email.
    
        Parameters:
        - user (User): The user object.
        - subject (str): The subject of the email.
        - message (str): The message body containing the OTP.
        """
        send_mail(subject, message, settings.EMAIL_HOST, [user.email])
        return True
    except Exception as e:
        return e


def get_user_by_identifier(identifier):
    """
    Retrieve a user by email or username.

    Parameters:
    - identifier (str): The email or username used to identify the user.

    Returns:
    - User: The user corresponding to the provided identifier.

    Raises:
    - Http404: If no user is found with the given identifier.
    """
    if '@' in identifier:
        # If '@' is present, assume the identifier is an email
        return get_object_or_404(UserModel, email=identifier)
    else:
        # Otherwise, assume the identifier is a username
        return get_object_or_404(UserModel, username=identifier)


def generate_otp():
    """
    Generate a six-digit OTP code.
    """
    return ''.join(random.choices('0123456789', k=6))
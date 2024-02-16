from django.db import models
from core_account.manager import CustomUserManager
from django.contrib.auth.models import AbstractUser,Group, Permission


class User(AbstractUser):
    # General Information about the user
    profile = models.ImageField(upload_to="profile/images", blank=True, null=True)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(null=False, unique=True)  
    date_of_birth = models.DateField(default=None, null=True)
    mobile_number = models.BigIntegerField(null=True)
    otp = models.PositiveIntegerField(null=True)
    otp_limit = models.IntegerField(null=True)
    otp_delay = models.TimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=None, null=True)
    is_blocked = models.BooleanField(default=False, null=True)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=200,db_index=True, default=None )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Remove 'email' from this list

    objects = CustomUserManager()

    # Unique related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions', blank=True)



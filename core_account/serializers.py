from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from core_account.utiles import generate_otp

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Validates password and confirms password match.
        """
        password = data.get('password')
        password2 = data.pop('password2', None)

        # Validate password strength
        validate_password(password)

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        """
        Creates a new user and generates OTP.
        """
        email = validated_data.pop('email', None)  # Remove email from validated_data
        if email is None:
            raise serializers.ValidationError({'email': 'Email field is required'})

        validated_data['username'] = validated_data.get('username')  # Ensure username is provided
        validated_data['password'] = validated_data.get('password')  # Ensure password is provided

        # Generate OTP
        otp = generate_otp() 
        # Save the user with OTP
        user = User.objects.create_user(email=email, otp=otp, **validated_data)
        return user

class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'date_of_birth', 'mobile_number', 'profile']
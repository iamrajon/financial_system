from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django_countries.fields import CountryField

User = get_user_model()   # get the customized model


class UserSignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        
        if password1 != password2:
            raise serializers.ValidationError("password fields didn't match!")
        
        password = attrs.get('password1')
        if len(password) < 8:
            raise serializers.ValidationError("Password must contain at least 8 characters!")
        return attrs
    
    def create(self, validated_data):
        # remove password1 and pasword2 and get password field only
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        user = User.objects.create_user(
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            password = password
        )
        return user
    

# serializer for UserLogin
class UserLoginSerializer(serializers.Serializer):
    # Password is write-only because we don't want to send it back in the response
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Email or Password!")
    
    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        

# serializer for UserLogout
class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return attrs
    
    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()   # Blacklist the refresh token and invalidate associated access tokens
        except Exception as e:
            raise serializers.ValidationError('Invalid token or token has already been blacklisted')


# Serializer for Updating and Retrieving User Profile
class UserProfileSerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name', required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'date_of_birth', 'citizenship_number', 
                  'country', 'province', 'city', 'zip_code']
        read_only_fields = ['email']  # email field is read-only ie it cannot be updated or changed

    


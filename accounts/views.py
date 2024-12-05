from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from .serializers import UserSignupSerializer, UserLoginSerializer, UserLogoutSerializer, UserProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()



# class based view for UserRegistration
class UserRegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles the User Registration.
        """
        serializer = self.get_serializer(data=request.data)  # Use `get_serializer` for consistency
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Registration Successful!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
"""
Explanation:
    - post(self, request): This handles the POST request. It initializes the serializer with the data from the request.
    - serializer.is_valid(): It checks whether the input data meets all validation rules.
    - serializer.save(): Calls the create() method of the serializer, creating the new user.
    - Response: A success or error response is returned depending on the validation result.
"""


# class based viw for User Login       
class UserLoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles User Login and return JWT tokens.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  # Authenticated user
            tokens = serializer.get_token_for_user(user)
            res = {
                'user': {
                    'username': user.username,
                    'email': user.email,
                },
                'tokens': tokens,
                'message': "User Login Successful!",
            }
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# class based view for UserLogout
class UserLogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles User Logout and blacklist the tokens.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Blacklist tokens
            return Response({"detail": "Logout Successful"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class based view for User Profile
class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
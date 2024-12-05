from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status

User = get_user_model()


# Test case for testing User Model- create_user method
class UserModelTest(TestCase):
    def test_create_user(self):
        email = "test.user1@gmail.com"
        username = "user1"
        password = "password1"

        user = User.objects.create_user(email=email, username=username, password=password)

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

# Test Case for UserRegisterView
class UserRegisterViewTest(APITestCase):
    def test_user_registration(self):
        url = reverse('user-signup')
        data = {
            'username': 'user2',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'test.user2@gmail.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], 'Registration Successful!')

# Test Case for UserLoginView
class UserLoginViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user2', password='testpassword123', email='test.user2@gmail.com')

    def test_user_login(self):
        url = reverse('user-login')  # Ensure this matches your URL pattern name
        data = {
            'email': 'test.user2@gmail.com',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['message'], 'User Login Successful!')

# Test Case for UserLogoutView
class UserLogoutViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.client.login(email='testuser@example.com', password='testpassword123')
        # Obtain tokens for the user
        self.refresh = RefreshToken.for_user(self.user)
        self.access = self.refresh.access_token

    def test_user_logout(self):
        url = reverse('user-logout')  # Ensure this matches your URL pattern name
        # Send the refresh token in the request data
        data = {
            'refresh': str(self.refresh)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Logout Successful')


# Test case for UserProfileView
class UserProfileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.client.login(username='testuser', password='testpassword123')
        self.refresh = RefreshToken.for_user(self.user)
        self.access = self.refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access}')

    def test_user_profile_retrieve(self):
        url = reverse('user-profile')  # Ensure this matches your URL pattern name
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_user_profile_update(self):
        url = reverse('user-profile')  # Ensure this matches your URL pattern name
        # Assuming 'country' is a field in your User model or related model
        data = {
            'username': 'updateduser',
            'phone_number': '9808748735',
            # Replace 'country' with the appropriate field name and value
            'country': 'USA'  # or use a primary key if it's a ForeignKey
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')
        self.assertEqual(response.data['phone_number'], '9808748735')
        





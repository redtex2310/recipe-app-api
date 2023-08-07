"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Allows us to get the URL from the view
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

# generic params allows to pass in any dictionary
# that can be pass to user
# We can pass any params that we want
def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


# Public test - Unauthenticated requests
# i.e registering user
class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # Create a http POST req with the above payload
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Validate that the email is actually created
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        # Check that password is not returned as response
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        # Make sure that the email already exist
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password is too short."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # Expect a bad request
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that user is not created in the db
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

def test_create_token_for_user(self):
    """Test generates token for valid credentials"""
    user_details = {
        'name': 'Test Name',
        'email': 'test@example.com',
        'password': 'test-user-password123',
    }
    create_user(**userdetails)

    payload = {
        'email': user_details['email'],
        'password': user_details['password'],
    }
    res = self.client.post(TOKEN_URL, payload)

    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)

def test_create_bad_credentials(self):
    """Test returns error if credentials is invalid."""
    create_user(email='test@example.com', password='goodpass')

    payload = {'email': 'test@example.com','password': 'badpass'}
    res = self.client.post(TOKEN_URL, payload)
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

def test_create_token_blank_password(self):
    """Test posting a blank password returns an error."""
    payload = {'email': 'test@example.com', 'password': ''}
    res = self.client.post(TOKEN_URL, payload)
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
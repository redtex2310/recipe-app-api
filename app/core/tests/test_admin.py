"""
Test for the Django admin modifications
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTest(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client"""
        # Creates Django test client. Allows for http req
        self.client = Client()
        self.admin_user = get_user_model().objects.create_user(
            email = 'admin@example.com',
            password = 'testpass123',
        )
        # Forces authentication for the created user
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'user@example.com',
            password = 'testpass123',
            name = 'Test User',
        )

    def test_users_list(self):
        """Test that users are listed on the page"""
        # Pulls URL page of list of users
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
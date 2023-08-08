"""
Views for the user API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializers,
    AuthTokenSerializer
)

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # Define the serializer associated with this view
    serializer_class = UserSerializers


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    # Customizing to use the created token authentication
    # serializer
    # ObtainAuthToken uses username and password instead
    # of email and password
    serializer_class = AuthTokenSerializer
    # Optional. Uses default. If not included we wont get
    # the browsable API. Will not show the nice UI otherwise
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializers
    # Use token authentication
    authentication_classes = [authentication.TokenAuthentication]
    # Make sure user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # Overrides the get object to only
    # retrieve the user that is authenticated
    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user
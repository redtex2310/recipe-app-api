"""
Views for the user API
"""
from rest_framework import generics
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



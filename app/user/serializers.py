"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers

# Creates model serializers
class UserSerializers(serializers.ModelSerializer):
    """Serializer for the user object."""

    # Tells drf the model and fields that we will pass
    class Meta:
        # Need to know what model to serialize
        model = get_user_model()
        # Minimum fields needed to pass. Only allow fields
        # that user can change through the API
        fields = ['email', 'password', 'name']
        # Extra param for each field
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # Allows to override method on the serializer when
    # a method is based on that serializer
    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # We want to use the create_user() method that we provide instead
        # of the serializer method.
        # This method will only be called if the validation is successful
        # ie password length < 5, method iwll not be called
        return get_user_model().objects.create_user(**validated_data)



class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        # Retieves email and password that the user provided
        # on the input
        email = attrs.get('email')
        password = attrs.get('password')
        # Authentication function from django.
        # checks username and password
        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password,
        )
        # Check that the user is set
        if not user:
            msg =  _('Unable to authenticate with provided credentials.')
            # The view will raise an http 401 error w/ error message
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
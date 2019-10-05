# This file is a modified version of
# https://github.com/jpadilla/django-jwt-auth/blob/master/jwt_auth/mixins.py

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.encoding import smart_text
from graphql_jwt.settings import jwt_settings as settings
import json
import jwt


jwt_decode_handler = settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class AuthenticationFailed(Exception):
    status_code = 401
    detail = 'Incorrect authentication credentials.'

    def __init__(self, detail=None):
        self.detail = detail or self.detail

    def __str__(self):
        return self.detail


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    From: https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/authentication.py
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')

    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode('iso-8859-1')

    return auth


class JSONWebTokenAuthMixin(object):
    """
    Token based authentication using the JSON Web Token standard.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string specified in the setting
    `JWT_AUTH_HEADER_PREFIX`. For example:
        Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            request.user, request.token = self.authenticate(request)
        except AuthenticationFailed as e:
            response = HttpResponse(
                json.dumps({'errors': [{"message": str(e)}]}),
                status=401,
                content_type='application/json'
            )
            response['WWW-Authenticate'] = 'JWT'

            return response
        except PermissionDenied as e:
            return HttpResponse(
                json.dumps({'errors': [{"message": str(e)}]}),
                status=403,
                content_type='application/json'
            )

        return super().dispatch(request, *args, **kwargs)

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
            raise AuthenticationFailed()

        if len(auth) == 1:
            msg = 'Invalid Authorization header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('Invalid Authorization header. Credentials string '
                   'should not contain spaces.')
            raise AuthenticationFailed(msg)

        try:
            payload = jwt_decode_handler(auth[1])
        except jwt.ExpiredSignature:
            msg = 'Signature has expired.'
            raise AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = 'Error decoding signature.'
            raise AuthenticationFailed(msg)

        user = self.authenticate_credentials(payload)
        if hasattr(self, 'check_authorization'):
            self.check_authorization(user)

        return user, auth[1]

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        try:
            username = jwt_get_username_from_payload(payload)

            if username:
                user = User.objects.get(username=username, is_active=True)
            else:
                msg = 'Invalid payload'
                raise AuthenticationFailed(msg)
        except User.DoesNotExist:
            msg = 'Invalid signature'
            raise AuthenticationFailed(msg)

        return user

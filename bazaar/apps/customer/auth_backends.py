from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from oscar.apps.customer.utils import normalise_email
import base64
import json

from oscar.core.compat import get_user_model

User = get_user_model()

# For EmailBackend
if hasattr(User, 'REQUIRED_FIELDS'):
    if not (User.USERNAME_FIELD == 'email' or 'email' in User.REQUIRED_FIELDS):
        raise ImproperlyConfigured(
            "EmailBackend: Your User model must have an email"
            " field with blank=False")

#For shibboleth
#from user.models import User
from django.contrib.auth.backends import RemoteUserBackend

class ShibbolethRemoteUserBackend(RemoteUserBackend):
    """
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """

    # Create a User object if not already in the database?
    create_unknown_user = True

    def authenticate(self, request_meta=None):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
	print repr(request_meta)
        print "Trying authenticate"
        if not request_meta:
            return None
        user = None
	if 'HTTP_USER_OID' not in request_meta:
            return None
	remote_user = request_meta['HTTP_USER_OID']
        username = self.clean_username(remote_user)
        data = request_meta['HTTP_USER_DATA']
        data = base64.b64decode(data)
        data = json.loads(data)
	print repr(data)
        if self.create_unknown_user:
	    defaults = {
	        'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': '%s@educloudalliance.org' % username,
                'oid': username,
	    }
            user, created = User.objects.get_or_create(username=username, defaults=defaults)
            if created:
                user = self.configure_user(user)
        else:
            try:
                user = User.objects.get(**shib_user_params)
            except User.DoesNotExist:
                pass
        print "Authenticating"
        return user


class EmailBackend(ModelBackend):
    """
    Custom auth backend that uses an email address and password

    For this to work, the User model must have an 'email' field
    """

    def authenticate(self, email=None, password=None, *args, **kwargs):
        if email is None:
            if 'username' not in kwargs or kwargs['username'] is None:
                return None
            clean_email = normalise_email(kwargs['username'])
        else:
            clean_email = normalise_email(email)

        # Check if we're dealing with an email address
        if '@' not in clean_email:
            return None

        # Since Django doesn't enforce emails to be unique, we look for all
        # matching users and try to authenticate them all. Note that we
        # intentionally allow multiple users with the same email address
        # (has been a requirement in larger system deployments),
        # we just enforce that they don't share the same password.
        matching_users = User.objects.filter(email=clean_email)
        authenticated_users = [
            user for user in matching_users if user.check_password(password)]
        if len(authenticated_users) == 1:
            # Happy path
            return authenticated_users[0]
        elif len(authenticated_users) > 1:
            # This is the problem scenario where we have multiple users with
            # the same email address AND password. We can't safely authenticate
            # either.
            raise User.MultipleObjectsReturned(
                "There are multiple users with the given email address and "
                "password")
        return None

# Deprecated in Oscar 0.8: Spelling
Emailbackend = EmailBackend

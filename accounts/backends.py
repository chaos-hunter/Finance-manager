from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

class EmailOrUsernameModelBackend(ModelBackend):
    """
        Authenticate using an email address first; on failure fall back
        to username lookup. Always return None if no single match.
        """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username:
            # Try email lookup first
            try:
                user = UserModel.objects.get(email__iexact=username)
            except UserModel.DoesNotExist:
                # No email match — let parent handle username lookup
                return super().authenticate(request, username, password, **kwargs)
            except MultipleObjectsReturned:
                # Ambiguous email: fail over to username lookup
                return super().authenticate(request, username, password, **kwargs)

            # We found exactly one user by email
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            return None

        return None
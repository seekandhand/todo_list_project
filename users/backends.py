from django.contrib.auth.backends import ModelBackend

from .models import CustomUser


class CustomBackend(ModelBackend):
    """
    Class that overrides default authentication backend
    """
    def authenticate(self, request, **kwargs):
        email = kwargs.get('email')
        organization = kwargs.get('organization')
        password = kwargs.get('password')

        try:
            user = CustomUser.objects.get(email=email, organization=organization)

            if getattr(user, 'is_active') and user.check_password(password):
                return user

        except CustomUser.DoesNotExist:
            pass

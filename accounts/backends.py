from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import CustomUser

class EmailOrPhoneBackend(ModelBackend):
    """
    Authenticate users with either Email, Phone number, or Username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email') or kwargs.get('phone')
        
        if not username:
            return None

        # Clean phone or username string
        login_credential = username.strip()

        try:
            # Query by email, phone, or username
            user = CustomUser.objects.filter(
                Q(email__iexact=login_credential) | 
                Q(phone__iexact=login_credential) |
                Q(username__iexact=login_credential)
            ).first()

            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception:
            return None

        return None

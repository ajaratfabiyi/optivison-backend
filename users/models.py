from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from .utils import generate_referral_code


class User(AbstractUser):
    """
    Custom User model with:
    - Referral system (mandatory for normal users signing up normally)
    - PIN for withdrawals
    - KYC status
    - 2FA flag
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    referred_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals'
    )
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    pin = models.CharField(max_length=6, blank=True, null=True)
    is_kyc_verified = models.BooleanField(default=False)
    two_fa_enabled = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # Auto-generate referral_code if empty
        if not self.referral_code:
            self.referral_code = generate_referral_code(self.username)

        # Skip referral validation for superusers, staff, or when creating superuser
        if not self.is_superuser and not self.is_staff:
            if not self.referred_by_id:
                raise ValidationError("A valid referral is required for non-admin users.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_referrals')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_referrals')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.referrer.email} referred {self.referred.email}"

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
import uuid
from .utils import generate_referral_code


class User(AbstractUser):
    """
    Custom User model with:
    - Referral system
    - Secure PIN for withdrawals
    - KYC status
    - 2FA support
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    referred_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals'
    )
    referral_code = models.CharField(max_length=10, unique=True, blank=True)

    # Withdrawal PIN (hashed)
    pin = models.CharField(max_length=255, blank=True, null=True)
    pin_reset_token = models.CharField(max_length=6, blank=True, null=True)

    # KYC
    is_kyc_verified = models.BooleanField(default=False)

    # 2FA
    two_factor_enabled = models.BooleanField(default=False)  # renamed for consistency
    two_factor_token = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_referral_code(self.username)

        if not self.is_superuser and not self.is_staff and not self.referred_by:
            raise ValidationError("A valid referral is required to create an account.")

        super().save(*args, **kwargs)

    # PIN helpers
    def set_pin(self, raw_pin):
        """Hash and store the PIN."""
        self.pin = make_password(raw_pin)
        self.save()

    def check_pin(self, raw_pin):
        """Verify the PIN."""
        if not self.pin:  # handle None
            return False
        return check_password(raw_pin, self.pin)

    def clear_pin_reset_token(self):
        """Clear the PIN reset token after use."""
        self.pin_reset_token = ""
        self.save()

    # 2FA helpers
    def clear_two_factor_token(self):
        """Clear the 2FA token after use."""
        self.two_factor_token = ""
        self.save()

    def __str__(self):
        return self.email


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_referrals')
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_referrals')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.referrer.email} referred {self.referred.email}"

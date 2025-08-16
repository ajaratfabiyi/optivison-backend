import uuid
import random
from django.core.mail import send_mail
from django.conf import settings


def generate_referral_code(username: str) -> str:
    """
    Generate a referral code from the first 3 letters of username + random UUID.
    Example: JOHAB12CD3
    """
    return username[:3].upper() + uuid.uuid4().hex[:7].upper()


def generate_otp(length: int = 6) -> str:
    """
    Generate a numeric OTP of given length.
    Default = 6 digits.
    """
    return "".join([str(random.randint(0, 9)) for _ in range(length)])


def send_otp_email(email: str, otp: str, subject: str = "Your Verification Code") -> None:
    """
    Send OTP via email.
    """
    message = f"Your verification code is: {otp}"
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=True,  # won’t crash if email backend isn’t configured
    )

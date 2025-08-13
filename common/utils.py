import uuid
import random
import string
from django.utils import timezone

def generate_unique_code(length=8, model=None, field_name=None):
    """
    Generates a unique alphanumeric code.
    If model and field_name are provided, ensures no duplicates in the DB.
    """
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if model and field_name:
            if not model.objects.filter(**{field_name: code}).exists():
                return code
        else:
            return code

def generate_uuid():
    """Returns a UUID4 string."""
    return str(uuid.uuid4())

def now():
    """Shortcut to get the current timezone-aware datetime."""
    return timezone.now()

def mask_email(email):
    """
    Masks part of an email for privacy.
    E.g. test@example.com -> t***@example.com
    """
    if not email or '@' not in email:
        return email or ''
    try:
        local, domain = email.split('@')
        if len(local) > 1:
            return local[0] + '***@' + domain
        return '***@' + domain
    except ValueError:
        return email

def mask_phone(phone):
    """
    Masks phone numbers except the last 2 digits.
    """
    if not phone or len(phone) < 3:
        return phone or ''
    return '*' * (len(phone) - 2) + phone[-2:]

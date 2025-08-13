def generate_referral_code(username):
    import uuid
    return username[:3].upper() + uuid.uuid4().hex[:7].upper()

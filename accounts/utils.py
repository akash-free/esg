import secrets
from django.utils import timezone
from datetime import timedelta

def generate_token():
    """Generate unique token for password set link"""
    token = secrets.token_urlsafe(32)
    print(f"Token generated: {token[:20]}...")
    return token

def create_set_password_token(user):
    """Create and save token for user"""
    print(f"create_set_password_token called for user: {user.email if user else 'None'}")
    
    if not user:
        print("ERROR: User is None!")
        return None
    
    user.set_password_token = generate_token()
    user.token_created_at = timezone.now()
    user.save()
    print(f"Token saved: {user.set_password_token[:20]}...")
    return user.set_password_token

def is_token_valid(user):
    """Check if token is still valid (7 days expiry)"""
    if not user.token_created_at:
        return False
    expiry = user.token_created_at + timedelta(days=7)
    return timezone.now() < expiry
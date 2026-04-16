from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from accounts.utils import create_set_password_token

def send_principal_set_password_email(principal_name, email, username, school_name, user):
    """Send email with direct set password link"""
    
    print("=" * 40)
    print("send_principal_set_password_email CALLED")
    print(f"Principal: {principal_name}")
    print(f"Email: {email}")
    print(f"School: {school_name}")
    print(f"User ID: {user.id if user else 'None'}")
    
    # Create token for this user
    print("Creating token...")
    try:
        token = create_set_password_token(user)
        print(f"Token created: {token}")
    except Exception as e:
        print(f"Token creation failed: {e}")
        return False
    
    # Direct set password link
    set_password_url = f"{settings.SITE_URL}/set-password/{token}/"
    print(f"Set password URL: {set_password_url}")
    
    context = {
        'name': principal_name,
        'school_name': school_name,
        'username': username,
        'set_password_url': set_password_url,
    }
    
    print("Rendering email template...")
    try:
        html_message = render_to_string('emails/principal_set_password.html', context)
        plain_message = strip_tags(html_message)
        print("Template rendered successfully")
    except Exception as e:
        print(f"Template rendering failed: {e}")
        return False
    
    subject = f'Set Your Password - Evolvu ESG Platform - {school_name}'
    print(f"Subject: {subject}")
    
    print("Sending email via SMTP...")
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        traceback.print_exc()
        return False
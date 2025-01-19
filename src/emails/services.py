from .models import Email


def verify_email(email):
    qs = Email.objects.filter(email=email, active=False)
    return qs.exists()

def start_verification_event(email):
   ver
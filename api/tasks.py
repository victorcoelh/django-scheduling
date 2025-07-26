from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_welcome_email(to_email):
    subject = "Confirm your registration."
    message = "This is a test e-mail."
    send_mail(subject, message, None, [to_email], fail_silently=False)

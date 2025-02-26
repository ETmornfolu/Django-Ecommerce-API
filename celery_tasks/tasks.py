from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_reset_password(email,reset_link):
    send_mail(
        subject='Password Reset',
        message=f'Click this link to reset your password {reset_link}',
        from_email='emmanuelmoronfolu6@gmail.com',
        recipient_list=[email],
        fail_silently=False
    )
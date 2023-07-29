from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_greeting_email(email):
    mail_subject = 'Welcome a new traveler.'
    message = 'Thank you for becoming part of our community. Enjoy YouTravel and all our trips'
    email_to_send = EmailMessage(
        mail_subject, message, to=[email]
    )
    return email_to_send.send()



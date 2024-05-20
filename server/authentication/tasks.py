from celery import shared_task
from .utils import Utils




@shared_task(name="password_reset_email_sending_task")
def password_reset_email_task(data):
    """
    Celery task for calling password reset email for sending email
    """
    try:
        Utils.send_password_reset_email(data)
    except Exception as e:
        print(f"An error occurred while running task --> {e}")


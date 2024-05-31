from celery import shared_task
from .utils import Utils


@shared_task(name="task_to_send_email_to_contacted_user")
def send_email_to_contacted_person(data):
    """
    Celery task for method to send email letting user know 
    that they have been contacted
    """
    try:
        Utils.send_email_to_user_notifying_user_has_been_contacted(data)
    except Exception as e:
        print(f"An error occurred while running task --> {e}")


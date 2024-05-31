
from .models import Portfolio
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from utils.exception.exception import CustomException as ce


# ! Signal for creating portfolio right after user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_porfolio_for_user(sender,**kwargs):
    """
    Creates Portfolio For Every Created User 
    """
    if kwargs['created']:
        Portfolio.objects.create(
            user=kwargs['instance']
        )


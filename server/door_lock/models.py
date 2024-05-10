from django.db import models
from rest_framework.fields import MaxValueValidator, MinValueValidator


# Create your models here.
class DoorLock(models.Model):
    """
    DoorLock model for database
    """

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    rfid = models.CharField(unique=True, blank=False, max_length=50)
    password = models.IntegerField(
        validators=[MinValueValidator(0000), MaxValueValidator(9999)]
    )

    def get_full_name(self):
        """
        Returns the full name of an object
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        prints the full name with rfid when we print its instance
        """
        return f"{self.first_name} {self.last_name} --- {self.rfid}"

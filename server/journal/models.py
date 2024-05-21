from django.db import models
from django.conf import settings
    



# ! Journal Model 
class Journal(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date=models.DateField(auto_now_add=True)
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='journal'
    )


    def __str__(self):
        """ 
        Returing string representation of the class Journal 
        """
        return self.title
    
    
    class Meta:
        """ 
        For keeping the user and date unique
        """
        unique_together = [['user', 'date']]
    




# ! Multiple Images For Journal Model
class JournalImage(models.Model):
    image=models.ImageField(upload_to='journal/')
    journal=models.ForeignKey(Journal,on_delete=models.CASCADE,related_name='images')


from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator



# ! Users Portfolio Model 
class Portfolio(models.Model):
    image=models.ImageField(upload_to='porfolio/', blank=True, null=True)
    description=models.TextField( blank=True, null=True)
    location=models.CharField(max_length=255, blank=True, null=True)
    instagram_link=models.CharField(max_length=255, blank=True, null=True)
    linkedin_link=models.CharField(max_length=255, blank=True, null=True)
    github_link=models.CharField(max_length=255, blank=True, null=True)
    contact_no=models.CharField(
        max_length=10,
        validators=[
            RegexValidator(r'^\d{10}$', 'Contact number must be exactly 10 digits and numeric.'),
        ], blank=True, null=True
    )
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        primary_key=True
    )




#! Education Model 
class Education(models.Model):
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True, null=True)
    date_from=models.DateField()
    date_to=models.DateField()
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='education'
    )


    def __str__(self) -> str:
        """
        Returing String Representation of object 
        """
        return self.institution_name
    



# ! Skills Model 
class Skill(models.Model):
    icon=models.CharField(max_length=255)
    name=models.CharField(max_length=255)
    level=models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='skill'
    )


    def __str__(self) -> str:
        """
        Returing String Representation of object 
        """
        return self.name
    



# ! Models For Projects 
class Project(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    live_link=models.CharField(max_length=255, blank=True, null=True)
    github_link=models.CharField(max_length=255, blank=True, null=True)
    user=models.ForeignKey(
      settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project'
    )


    def __str__(self) -> str:
        """
        Returing String Representation of object 
        """
        return self.title
    



# ! Contact Model
class Contact(models.Model):
    fullname=models.CharField(max_length=255)
    email=models.EmailField()
    subject=models.CharField(max_length=255)
    message=models.TextField()
    date=models.DateField(auto_now_add=True)
    contact_no=models.CharField(
        max_length=10,
        validators=[
            RegexValidator(r'^\d{10}$', 'Contact number must be exactly 10 digits and numeric.'),
        ]
    )


    def __str__(self) -> str:
        """
        Returing String Representation of object 
        """
        return self.fullname

    














    



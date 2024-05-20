from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings




class Utils:
    @staticmethod
    def send_password_reset_email(data):
        """
        Method for sending password reset email
        """
        try:
            email=data['to_email']
            subject=data['subject']
            link=data['link']

            context={
                'link':link
            }
            message=render_to_string('emails/password_reset_email.html',context)

            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [email],html_message=message)
            
        except Exception as e:
            print(f"Some Error occrured during sending email {e}")
        
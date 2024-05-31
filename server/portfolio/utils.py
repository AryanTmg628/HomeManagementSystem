from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings




class Utils:
    @staticmethod
    def send_email_to_user_notifying_user_has_been_contacted(data):
        """
        Method for sending password reset email
        """
        try:
            to_email=data['to_email']
            subject=data['subject']
            message=data['message']
            fullname=data['fullname']
            date=data['date']
            user_email=data['email']
            contact_no=data['contact_no']
            
            context={
                'subject':subject,
                'message':message,
                'fullname':fullname,
                'date':date,
                'user_email':user_email,
                'contact_no':contact_no
            }

            message=render_to_string('portfolio/contact_email.html',context)

            send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [to_email],html_message=message)
            
        except Exception as e:
            print(f"Some Error occrured during sending email {e}")
        
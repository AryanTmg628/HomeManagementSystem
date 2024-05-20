from .models import User
from .tasks import password_reset_email_task
from utils.exception.exception import CustomException as ce 


from rest_framework import serializers


from django.utils.encoding import smart_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode




# ! User Registration Serailizer 
class UserRegistrationSerailizer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )
    password_confirmation=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )


    class Meta:
        model=User 
        fields=[
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password_confirmation'
        ]


    def validate(self, attrs):
        """
        Validating two passwords field
        """
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')

        if password!=password_confirmation:
            raise ce(
                message="Two password doesn't match"
            )
        return attrs 
    

    def create(self,validated_data):
        """
        Over-riding the create method to create a user
        account 
        """
        try:       
            user=User.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'],
                email=validated_data['email'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user 
            
        except Exception as e:
            raise ce(
                message="Some Error occoured during registration"
            )
        



# !  User Login Serailizer 
class UserLoginSerailizer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        # validators=[validate_password]
    )




# ! User ChangePassword  
class UserChangePasswordSerailizer(serializers.Serializer):
    old_password=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )
    new_password=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )
    new_password_confirmation=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )


    def validate_old_password(self,value):
        """
        Validation for Checking if old password matches or not 
        """
        user=self.context['user']
        
        if not user.check_password(value):
            raise ce(
                message="Your current password doesn't match",
                )
        
        return value
    

    def validate(self, attrs):
        """
        Extra Validation of New Password and Old Password
        with New Password
        """
        old_password=attrs.get('old_password')
        new_password=attrs.get('new_password')
        new_password_confirmation=attrs.get('new_password_confirmation')

        if new_password != new_password_confirmation:
            raise ce(
                message='Two Passwords does not match'
            )
        
        if old_password==new_password:
            raise ce(
                message="New passwords cannot be similar to current password "
            ) 
        
        # ! Changing the users password here
        user=self.context['user']
        user.set_password(new_password)
        user.save()
        return attrs 
    
    


# ! Send Password Reset email serailizer
class SendPasswordResetEmailSerailizer(serializers.Serializer):
    email=serializers.EmailField()

    def validate_email(self,value):
        """
        Check for account with the received email and creates
        uid and token for user 
        """
        try:
            user=User.objects.get(email=value)
        except User.DoesNotExist:
            raise ce(
                message="User with the given email doesn't exist"
            )
        
        # ! Generate uid and tokens for user
        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)

        # ! Generated data for sending in mail 
        link=f'http://127.0.0.1:8000/api/auth/reset-password/{uid}/{token}/'
        subject="Resetting Password"
        email=user.email

        data={
            'link':link,
            'to_email':email,
            'subject':subject
        }

        # ! Celery task for sending password reset email is called
        password_reset_email_task.delay(data)
        return value




# ! User Reset Password  
class UserPasswordResetSerailizer(serializers.Serializer):
    password=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )
    password_confirmation=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )


    def validate(self, attrs):
        """
        Validating two passwords field and setting password 
        for the user if uid and tokens matches
        """

        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')

        uid=self.context['uid']
        token=self.context['token']
        user_id=smart_str(urlsafe_base64_decode(uid))

        # ! password validation
        if password!=password_confirmation:
            raise ce(
                message="Two password doesn't match"
            )
        
        # ! Checks if thne token received matches with the token generated for user
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise ce(
                message="Token Expired or Invalid"
            )
        
        try:
            user=User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ce(
                message="User with the given email doesn't exist"
            )
         
        # ! Sets the new password and saves it 
        user.set_password(password)
        user.save()
        return attrs
        





    




    


    
    
    




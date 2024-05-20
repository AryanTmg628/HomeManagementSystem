from rest_framework_simplejwt.tokens import RefreshToken


#! Generates token manually
def get_tokens_for_user(user):
    """
    Custom function to generate and return access and
    refresh tokens for a user after successful login
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access': str(refresh.access_token),
    }
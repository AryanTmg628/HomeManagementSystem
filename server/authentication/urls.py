from django.urls import path

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserChangePasswordView,
    SendPasswordResetEamilView,
    UserPasswordResetView
)

urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='user-register'),
    path('login/',UserLoginView.as_view(),name='user-login'),
    path('change-password/',UserChangePasswordView.as_view(),name='user-change-password'),
    path('forgot-password/',SendPasswordResetEamilView.as_view(),name='send-password-reset-email'),
    path('reset-password/<str:uid>/<str:token>/',UserPasswordResetView.as_view(),name='reset-password'),
]

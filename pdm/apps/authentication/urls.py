from django.urls import path
from .views import (
AddUserAPIView,
UserLoginAPIView
)

urlpatterns = [
    path('register/user', AddUserAPIView.as_view(), name="register_user"),
    path('login', UserLoginAPIView.as_view(), name="login")
]

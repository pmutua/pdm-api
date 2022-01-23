from django.urls import path
from .views import (
AddUserAPIView
)

urlpatterns = [
    path('register/user', AddUserAPIView.as_view(), name="register_user")
]

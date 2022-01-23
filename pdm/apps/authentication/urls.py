from django.urld import path
from .views import (
AddUserAPIView
)

patterns = [
    path('register/user', AddUserAPIView.as_view(), name="register_user")
]

from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import *


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name"]


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "identification_no",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "identification_no",
            "groups",
            "last_login"
]


class UserLoginSerializer(serializers.Serializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    password = serializers.CharField()
    username = serializers.CharField()
    dept = serializers.IntegerField()

    class Meta:
        fields = [
            "username",
            "org",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("id",)

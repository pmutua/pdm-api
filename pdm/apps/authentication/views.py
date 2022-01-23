from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.template import loader
from django.utils.html import strip_tags
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from pdm.apps.authentication.models import Department, User
from .custom_jwt import jwt_encode_handler, jwt_payload_handler

from .serializers import (
    UserDetailSerializer,
    UserLoginSerializer,
    UserSerializer,
)

from .tasks import send_credentials


class AddUserAPIView(APIView):
    """register self service NOTE An organization must EXIST!!"""

    # permission_classes = (permissions.AllowAny,)

    """register
    {
        "first_name": "admin",
        "last_name": "admin",
        "email": "youremail.example.com",
        "roles": ["chief","admin"],
        "phone": "7777",
        "identification_no": "747474",
        "department": "Ministry of Uganda"
    }
    """

    def post(self, request, *args, **kwargs):
        roles_ = []
        grps = []
        req = request.data

        for role in request.data.get("roles"):
            grp, _ = Group.objects.get_or_create(name=role)
            grps.append(grp)

        for x in request.data.get("roles"):
            r, _ = Group.objects.get_or_create(name=x)
            roles_.append(r)

        if User.objects.filter(email=request.data.get("email")).exists() is True:
            res = {
                "msg": "User with the email {} already registered.".format(request.data.get("email")),
                "data": None,
                "success": False,
            }
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


        department,_ = Department.objects.get_or_create(name=request.data.get("department"))

        serializer = UserSerializer(data=req)
        # Validate payload
        if serializer.is_valid():

            try:

                new_user = User.objects.create(
                    username=req.get("email"),
                    email=req.get("email"),
                    first_name=req.get("first_name").capitalize(),
                    last_name=req.get("last_name").capitalize(),
                    is_active=True,
                    phone=request.data.get("phone"),
                    identification_no=req.get("identification_no"),
                    dept_id=department.id,
                    is_staff=False,
                )

                [new_user.groups.add(grp) for grp in grps]

                # Create Random Password
                password = User.objects.make_random_password(length=10)

                new_user.set_password(password)
                new_user.save()

                login_site = settings.LOGIN_REDIRECT_URL

                ctx = {
                    "dept_name": department.name,
                    "username": new_user.email,
                    "password": password,
                    "link": login_site,
                    "user_email": new_user.email,
                }

                # client_html_message = loader.render_to_string("authentication/email-user-creds.html")
                #
                # client_message_string = strip_tags(client_html_message)
                #
                # client_html_content = loader.render_to_string("authentication/email-user-creds", ctx)
                #
                # client_message = {"html": client_html_content, "text": client_message_string}
                #
                # department.users.add(new_user)
                # department.save()
                # serializer = UserSerializer(new_user)
                #
                # send_mail_to_admin = send_credentials(
                #     "Welcome onboard {}".format(department.name), client_message, new_user.email
                # )

                ser = UserDetailSerializer(new_user)

                res = {
                    "msg": "You have successfully registered. Check your email for login information",
                    "data": ser.data,
                    "success": True,
                }
                return Response(data=res, status=status.HTTP_201_CREATED)
            except Exception as e:
                res = {"msg": str(e), "data": None, "success": False}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        res = {"msg": str(serializer.errors), "data": None, "success": False}
        return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(generics.CreateAPIView):
    """Class base view for new user."""

    # permission_classes = [permissions.AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        """Creates a new user."""

        try:
            user = User.objects.get(email=request.data["email"])
            dept = Group.objects.get(id=user.org_id)

        except Exception as e:
            res = {"msg": str(e), "success": False, "data": None}
            return Response(data=res, status=status.HTTP_200_OK)

        if check_password(request.data["password"], user.password):
            payload = jwt_payload_handler(user, dept)

            token = jwt_encode_handler(payload)

            user.last_login = settings.CURRENT_DATE_TIME
            user.save()
            roles = [{"id": role.id, "name": role.name} for role in user.groups.all()]
            fullname = user.first_name + " " + user.last_name
            res = {
                "msg": "Login success",
                "success": True,
                "data": {
                    "name": fullname,
                    "username": user.username,
                    "id": user.id,
                    "token": token,
                    "roles": roles,
                    "phone": user.phone,
                },
            }
            return Response(data=res, status=status.HTTP_200_OK)

        else:
            res = {"msg": "Invalid login credentials", "data": None, "success": False}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

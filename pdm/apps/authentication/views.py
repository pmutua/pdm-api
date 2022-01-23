from django.contrib.auth.models import(
    Group,
    AbstractUser,
    Permission,
)
from datetime import date
import uuid
from rest_framework_jwt.settings import api_settings
from django.conf import settings
from django.db import models

from django.utils import timezone
from datetime import datetime
from datetime import timedelta

from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.contenttypes.models import ContentType

import os
import uuid
import random

from datetime import datetime


import pytz

utc=pytz.UTC


from cloudinary_storage.storage import RawMediaCloudinaryStorage
# Create your models here. OTP
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from .utils import unique_otp_generator

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager
import random
import os
import requests

from django.views.decorators.cache import cache_page


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            phone=phone
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,


        )
        return user

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user



def objection_directory_path(instance, filename):
    # Get Current Date
    todays_date = datetime.now()

    path = "objections/{}/{}/{}/".format(todays_date.year, todays_date.month, todays_date.day)
    extension = "." + filename.split('.')[-1]
    stringId = str(uuid.uuid4())
    randInt = str(random.randint(10, 99))

    # Filename reformat
    filename_reformat = stringId + randInt + extension

    return os.path.join(path, filename_reformat)

class Status(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name is None:
            return 'N/A'
        return self.name

class Town(models.Model):
    name = models.CharField(unique=True,max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Fee(models.Model):
    line_fee_id = models.CharField(max_length=255,blank=True,null=True)
    line_income_type = models.CharField(max_length=255,blank=True,null=True)
    line_chart_account_no = models.CharField(max_length=255,blank=True,null=True)
    cost_centre = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(null=True, blank=True)
    code = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Organization(Group):
    email = models.EmailField(max_length=60, blank=False, null=False)
    admin = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='org_users',blank=True)
    is_active = models.BooleanField(default=True)
    short_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    tag_line = models.TextField(null=True, blank=True)
    company_phone = models.CharField(max_length=15, blank=True, null=True)
    po_box = models.CharField(max_length=15, blank=True, null=True)
    logo = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name +"ID-"+ str(self.id)


class Role(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        if self.name is None:
            return "None"
        return self.name


class User(AbstractUser):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    id = models.CharField(max_length=100, unique=True,default=uuid.uuid4, primary_key=True)
    roles = models.ManyToManyField(Role, blank=True)
    org_id = models.IntegerField(null=True, blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    identification_no = models.CharField(max_length=100,blank=True,null=True)
    first_login = models.BooleanField(default=False)
    # timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        if self.id is None:
            return 'N/A'
        return f"{self.first_name} {self.last_name}"


    # USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = []

    # objects = UserManager()

    # def __str__(self):
    #     return self.phone

    # def get_full_name(self):
    #     return self.phone

    # def get_short_name(self):
    #     return self.phone

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):

    #     return True

    # @property
    # def is_staff(self):
    #     return self.staff

    # @property
    # def is_admin(self):
    #     return self.admin

    # @property
    # def is_active(self):
    #     return self.active




    @property
    def online(self):
        if self.last_login is not None:
            now = settings.CURRENT_DATE
            if utc.localize(now) > self.last_login + timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False 

class FileUpload(models.Model):
    """Represents Csv class model"""
    file_name = models.FileField(upload_to='csv/')
    uploaded = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=255,blank=True,null=True)
    size = models.CharField(max_length=255,blank=True,null=True)
    url = models.CharField(max_length=255,blank=True,null=True)
    activated = models.BooleanField(default=False)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'File id: {self.id}'


    @property
    def name(self):
        return self.file_name.name[5:]


class Property(models.Model):
    """Represents propertyclass model"""
    serial_no = models.CharField(unique=True,max_length=255,blank=True,null=True)
    map_no = models.CharField(max_length=255,blank=True,null=True)
    lr_no =  models.CharField(max_length=255,blank=True,null=True)
    locality =  models.CharField(max_length=255,blank=True,null=True)
    city =  models.CharField(max_length=255,blank=True,null=True)
    situation =  models.CharField(max_length=255,blank=True,null=True)
    owner =  models.CharField(max_length=255,blank=True,null=True)
    po_box = models.CharField(max_length=255,blank=True,null=True)
    postal_code = models.CharField(max_length=255,blank=True,null=True)
    address =  models.CharField(max_length=255,blank=True,null=True)
    approx_area = models.FloatField(blank=True,null=True)
    usv = models.BigIntegerField(null=True,blank=True)
    land_use  = models.CharField(max_length=255,blank=True,null=True)
    year = models.IntegerField(blank=True,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_objected = models.BooleanField(default=False,null=True,blank=True)
    bill_no = models.CharField(max_length=255,blank=True,null=True)


    def __str__(self):
        if self.id is None:
            return 'N/A'
        return str(self.id)



class Reason(models.Model):
    description = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.description is None:
            return 'N/A'
        return self.description


class Document(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    objection_no = models.CharField(max_length=255,null=True, blank=True)
    file = models.FileField(upload_to='objections/',storage=RawMediaCloudinaryStorage())
    size = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.id is None:
            return 'N/A'
        return f'File id: {self.id}'


class PropertyObjection(models.Model):
    objection_no = models.CharField(max_length=255,null=True, blank=True)
    status =  models.ForeignKey(Status, on_delete=models.CASCADE,null=True,blank=True)
    ratable_owner = models.BooleanField(null=True,blank=True)
    ratable_relation = models.CharField(max_length=255,null=True, blank=True)
    objector = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    properties =  models.ManyToManyField(Property,blank=True)
    reasons = models.ManyToManyField(Reason,blank=True)
    documents = models.ManyToManyField(Document,blank=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    phone = models.CharField(max_length=255,null=True, blank=True)
    postal_address = models.CharField(max_length=255,null=True, blank=True)
    total_charge =  models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True)
    objection_date= models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


    @property
    def objector_name(self):
        po = Bill.objects.filter(objection_no=self.objection_no)
        if po.exists() is True:
            state_,_ = Status.objects.get_or_create(name="Paid")
            if po[0].is_paid is True:
                self.status = state_
                self.save()
            return '{} {}'.format(self.objector.first_name,self.objector.last_name)
        return '{} {}'.format(self.objector.first_name,self.objector.last_name)


class WithdrawnProperty(models.Model):
    """Represents Property Objection."""
    property_objection = models.ForeignKey(PropertyObjection,null=True,blank=True,on_delete=models.CASCADE)
    withdrawn_by = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    property_objected = models.ForeignKey(Property,null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return f'OBJECTION_NO: {self.property_objection.objection_no}--OBJECTED BY: {self.withdrawn_by.first_name}---PROPERTY_LR_NO: { self.property_objected.lr_no}'


class BillType(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BillItem(models.Model):
    """Represents bill Item."""
    description = models.TextField()
    amount = models.DecimalField(max_digits=12,decimal_places=2, null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description+ " "+ str(self.amount)

    
class Bill(models.Model):
    """Represents a bill class model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    state = models.ForeignKey(Status, on_delete=models.CASCADE,null=True,blank=True)
    bill_items = models.ManyToManyField(BillItem,blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    bill_type = models.ForeignKey(BillType, on_delete=models.CASCADE,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    valid_from = models.DateField(null=True,blank=True)
    bill_no = models.CharField(max_length=250, null=True, blank=True)
    objection_no = models.CharField(max_length=250, null=True, blank=True)
    is_voided = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=250, null=True, blank=True)
    modified_at = models.DateTimeField(default=timezone.now)

    @property
    def billed_user(self):
        if self.user is None:
            return "None"
        return '{} {}'.format(self.user.first_name, self.user.last_name)


    @property
    def total(self):
        result = sum([billitm.amount for billitm in self.bill_items.all()])
        return result

    @property
    def status(self):

        amount_found = sum([float(obj.amount) for obj in Payment.objects.filter(bill_number=self.bill_no)])
        total= sum([int(float(item.amount)) for item in self.bill_items.all()])

        if amount_found ==0:
            return "UnPaid"
        if float(amount_found) < total and float(amount_found) > 0:
            return "PartiallyPaid"
        if amount_found == total:
            self.is_paid=True
            self.save()
            return "Paid"
        if amount_found > total:
            return "OverPaid"




class Receipt(models.Model):
    """Represents receipt class"""
    bill= models.ForeignKey(Bill,on_delete=models.CASCADE,null=True, blank=True)
    receipt_no = models.CharField(unique=True,max_length=250, null=True, blank=True)
    payment_mode = models.CharField(max_length=250, null=True, blank=True)
    description  = models.TextField(max_length=250, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=12,decimal_places=2, null=True,blank=True)
    date_recieved = models.DateTimeField(null=True, blank=True)
    paid_by = models.CharField(max_length=250,null=True,blank=True)
    paid_to = models.CharField(max_length=250,null=True,blank=True)
    created_by = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    @property
    def billed_user(self):
        if self.bill.user is None:
            return "None"
        return '{} {}'.format(self.bill.user.first_name, self.bill.user.last_name)

    @property
    def bill_total(self):
        bill_total = sum([billitm.amount for billitm in self.bill.bill_items.all()])
        return bill_total


    @property
    def balance(self):
        payments = Payment.objects.filter(bill_number=self.bill.bill_no)
        bill_total = sum([billitm.amount for billitm in self.bill.bill_items.all()])
        if len(payments) == 0:
            return bill_total
        
        payment_total = sum([ p.amount for p in payments])
        bal = bill_total - payment_total
        return bal



class Payment(models.Model):
    """Represents payment model class"""
    reference_number = models.CharField(max_length=250,null=True,blank=True)
    bill_number = models.CharField(max_length=250,null=True,blank=True)
    amount = models.BigIntegerField(null=True,blank=True)
    receipt_number = models.CharField(max_length=250,null=True,blank=True)
    payment_date= models.DateTimeField(null=True, blank=True)
    payment_mode = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.receipt_number +" "+ str(self.amount)



class Log(models.Model):
    """Represents class model for system logs"""
    LOG_TYPE_CHOICES = (
        ("celery_task_records_upload", ("celery_task_records_upload")),
        ("celery_task", ("celery_task")),
        ("response", ("response")),
        ("access", ("access")),
        ("payment_callback", ("payment_callback"))
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True,blank=True)
    log_type = models.CharField(max_length=50, choices=LOG_TYPE_CHOICES, null=True, blank=True)
    description = models.TextField(null=True,blank=True)
    ip_address = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Formats
            [2021-01-28 11:49:58 +0300] [9] [INFO] Booting worker with pid: 9
        """
        userid =None
        if self.user is None:
            userid = "NONE"
        else:
            userid = str(self.user.id)
        return '['+str(self.created_at) + ']'+' ' +'USER_ID-'+userid+' '+str(self.ip_address) +' '+ '[INFO]'+ " "+self.description


# class PropertyViewed(models.Model):
#     user = models.ForeignKey(User,blank=True,null=True)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type','object_id')

#     def -_str__(self)


class PropertySearchTracker(models.Model):
    """tracks user search activity"""
    searched_property = models.ForeignKey(Property,on_delete=models.CASCADE,blank=True,null=True)
    ip_address = models.CharField(max_length=250)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    count= models.BigIntegerField(default=0,null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'[OWNER]-{self.searched_property.owner}-[LR_NO]-{self.searched_property.lr_no }[LR_NO]-{self.searched_property.serial_no }-[COUNT]-{self.count}'






class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)



class LandUse(models.Model):
    description = models.CharField(max_length = 255, blank = True, null= True)

    def __str__(self):
        return self.description
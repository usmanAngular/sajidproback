from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


# Create your models here.

class User_Profile(models.Model):
    ROLE_CHOICES = (
        ('A', 'Admin'),
        ('S', 'Support Coordinator'),
        ('C', 'Customer'),
        ('O', 'Order Coordinator'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='0')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True)
    location=models.CharField(max_length=255,blank=True)
    phone=models.CharField(max_length=255,blank=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='C')
    verfication_status = models.BooleanField(default=False)
    registration_status = models.BooleanField(default=False, blank=True)
    user_deactive_status=models.CharField(max_length=255, blank=True, default='')
    user_deactive_reason=models.CharField(max_length=255, blank=True, default='')
    forget_password_key=models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user)

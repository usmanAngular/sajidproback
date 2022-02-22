from django.contrib.auth import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


# Create your models here.
class Services_Type(models.Model):
    services_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.services_name)

class Services_Level(models.Model):
    services_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.services_name)

class Paper_type(models.Model):
    paper_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.paper_name)


class Pricing(models.Model):
    services_type=models.ForeignKey(Services_Type,related_name='services_type', on_delete=models.CASCADE)
    services_level=models.ForeignKey(Services_Level,related_name='services_level', on_delete=models.CASCADE)
    paper_type=models.ForeignKey(Paper_type,related_name='paper_type', on_delete=models.CASCADE)
    price= models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.services_type)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    order_price=models.CharField(max_length=255)
    total_pages = models.CharField(max_length=255, default='1')
    media_file=models.FileField(upload_to='media/order_media')
    topic=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    deadline=models.DateField()
    pricing= models.ForeignKey(Pricing, related_name='pricing',on_delete=models.CASCADE, default='0')
    total_price=models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.topic)


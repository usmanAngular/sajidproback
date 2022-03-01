from django.contrib.auth import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


# Create your models here.
class Services_Type(models.Model):
    services_type_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.services_type_name)

class Services_Level(models.Model):
    services_level_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.services_level_name)

class Paper_type(models.Model):
    paper_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.paper_name)


class Pricing(models.Model):
    days = (
        ('2',  '2 Days'),
        ('10', '10 Days'),
        ('20', '20 Days'),
        ('30', '30 Days'),
    )

    services_type=models.ForeignKey(Services_Type,related_name='services_type', on_delete=models.CASCADE)
    services_level=models.ForeignKey(Services_Level,related_name='services_level', on_delete=models.CASCADE)
    paper_type=models.ForeignKey(Paper_type,related_name='paper_type', on_delete=models.CASCADE)
    price= models.CharField(max_length=255)
    deadline = models.CharField(max_length=255,choices=days, default='2')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.services_type)


class Order(models.Model):
    orderstatus = (
        ('S', 'Start'),
        ('C', 'Completed'),
        ('P', 'In Process'),
        ('N', 'None'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='0')
    order_price=models.CharField(max_length=255)
    total_pages = models.CharField(max_length=255, default='1')
    media_file=models.FileField(upload_to='media/order_media')
    topic=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    deadline=models.DateField()
    actual_price=models.CharField(max_length=255)
    pricing= models.ForeignKey(Pricing, related_name='pricing',on_delete=models.CASCADE, default='0')
    total_price=models.CharField(max_length=255)
    order_status=models.CharField(max_length=1, choices=orderstatus, default='N')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.topic)

class Coupen(models.Model):
    coupen_name = models.CharField(max_length=255)
    coupen_code=models.CharField(max_length=255)
    coupen_fixed_price=models.CharField(max_length=255,blank=True,null=True)
    coupen_percentage_price=models.CharField(max_length=255,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.coupen_name)
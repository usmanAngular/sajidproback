from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import User_Profile
from rest_framework import serializers

from services.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields= "__all__"




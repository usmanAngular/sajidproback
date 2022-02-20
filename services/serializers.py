from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import User_Profile
from rest_framework import serializers

from services.models import Order, Pricing,Paper_type,Services_Level

class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pricing
        fields= "__all__"

class OrderSerializer(serializers.ModelSerializer):

    pricing = PricingSerializer()
    class Meta:
        model=Order
        fields= ["topic","pricing"]
        # fields= "__all__"
        # extra_field=["services_type"]


class ServicesLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Services_Level
        fields= "__all__"


class PaperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Paper_type
        fields= "__all__"










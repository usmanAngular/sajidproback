from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import User_Profile
from rest_framework import serializers

from core.models import User_Profile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_Profile
        fields= "__all__"




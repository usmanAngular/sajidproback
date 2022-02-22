import random
import re
import string
# from _multiprocessing import send
from datetime import datetime, tzinfo
from datetime import timedelta
import datetime
from django.utils import timezone
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.db import transaction, IntegrityError
from google.auth.transport._http_client import Response
# from numpy import all
from rest_framework.utils import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

import core
import re
import string
# from _multiprocessing import send
from datetime import datetime, tzinfo
from datetime import timedelta
import datetime
from django.utils import timezone
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMessage
from django.db import transaction, IntegrityError
from google.auth.transport._http_client import Response
from rest_framework.utils import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

import core
# from .serializers import *
from .serializers import *
from rest_framework import status, viewsets, mixins, generics, response
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Generate Jwt-Token
from rest_framework_jwt.settings import api_settings
wt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from datetime import datetime, timezone



class Order_Class(viewsets.ViewSet):#Place order
    # {
    #     "order_price": "farz.mirza@argonteq.com",
    #     "media_file": "MMMirza@1213AAA"
    # }

    @action(detail=False,methods=['post','get'])
    def Place_order(self, request):
        if request.method == "POST":
            data=request.data
            data['user']=request.user.id
            serializer = SaveOrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Successfully'}, status.HTTP_200_OK)
            else:
                print(serializer.errors)
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "GET":
            all_order=Order.objects.all()
            print(all_order)
            serializer = OrderSerializer(all_order, many=True)
            return Response({"AllProfiles": serializer.data})

    @action(detail=False, methods=['get'])
    def all_services(self, request):
        all_services = Pricing.objects.all()
        serializer = PricingSerializer(all_services, many=True)
        return Response({"All Services": serializer.data})

    @action(detail=False, methods=['post'])
    def price_calulator(self, request):
        if request.method == "POST":
            pages=request.data['pages']
            get_service = Pricing.objects.get(id=request.data['pricing'])
            calculated_price=int(get_service.price)*int(pages)
            return Response({"Service Price": calculated_price})














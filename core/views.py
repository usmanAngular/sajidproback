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
from .core_functions import generateOTP, days_hours_minutes, twilio_otp, otp_verification_check, Pagination, qdict_to_dict
# from .serializers import *
from .serializers import *
from rest_framework import status, viewsets, mixins, generics, response
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Generate Jwt-Token
from rest_framework_jwt.settings import api_settings
wt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from password_strength import PasswordPolicy, stats
from password_strength import PasswordStats
from datetime import datetime, timezone
policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)


policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)

#=========================Function start
def emailsending(key,template,email,msg):
    message = get_template(template).render(key)
    email = EmailMessage(msg, message, to=[email])
    email.content_subtype = 'html'
    email.send()
    print('Email Send Successfully')


def password_strenght(password):
    stats = PasswordStats(password)
    strenght = stats.strength()
    print(strenght)
    return strenght

def isNum(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def set_if_not_none(mapping, key, value):
    if value is not None:
        mapping[key] = value


#================================Views Start

class User_Profiles(viewsets.ViewSet):#User class
    # {
    #     "email": "farz.mirza@argonteq.com",
    #     "password": "MMMirza@1213AAA"
    # }

    @action(detail=False,methods=['post'])
    def user_login(self, request):
        # host=request.META['HTTP_ORIGIN']
        username=request.data["email"]
        password=request.data["password"]

        if (User.objects.filter(username=username).exists()):
            object_user = User.objects.get(username=username)
            user_profile_object = User_Profile.objects.get(user=object_user.id)

            newapi='http://127.0.0.1:8000/core/login/'
            # newapi='http://18.118.201.66/core/login/'
            data1 = {"username": object_user.username,
                     "password": password}


            response = requests.post(newapi, data=data1).json()
            if 'token' in response:
                key = response['token']
                return Response({"Token": key, "Role": user_profile_object.role,"Verfication_Status":user_profile_object.verfication_status}, status=status.HTTP_200_OK)

            else:
                return Response({"Message": "Wrong password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Message": "Email does not Exist"}, status=status.HTTP_404_NOT_FOUND)

    # {
    #     "email": "farz.mirza@argonteq.com",
    #     "password": "MMMirza@1213AAA",
    #     "phone": "546567"
    # }


    @action(detail=False, methods=['post','put'])
    def signup(self,request):#user_login
        if request.method=="POST":
            if User.objects.filter(Q(username=request.data['email'])).exists():
                return Response({"msg": "Already Registered"}, status.HTTP_306_RESERVED)
            else:
                user = User.objects.create_user(
                            username=request.data['email'],
                            password=request.data['password']

                )
                if user != '':

                    email = request.data['email']
                    user = User.objects.get(username=email)
                    data={"user":user.id,"registration_status":False}
                    if 'phone' in request.data:
                        data['phone']=request.data['phone']
                    print(data)
                    serializer = UserProfileSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        # emailsending(otp, 'Activation_Email.html', email, 'Email Confirmation')
                        return Response({'Message': 'Successfully'}, status.HTTP_200_OK)
                    else:
                        print(serializer.errors)
                        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'Message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


        if request.method=="PUT":# Update User profile
            try:
                user_obj = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                return Response({"Message":"User does not exist"},status=status.HTTP_404_NOT_FOUND)


            profile_obj = request.data
            print(profile_obj,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            serializer = ProfilePostSerializer(user_obj,data=profile_obj,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Update Profile Successfully!'}, status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes((IsAuthenticated,))
    @action(detail=False, methods=['put','post'])
    def otp(self,request):
        # print(request.user)
        if request.method == "PUT":# Resend OTP
            try:
                user_obj = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                # print("***************")
                if "email" in request.data and User.objects.filter(username=request.data['email']).exists():
                    user_obj = User.objects.get(username=request.data['email'])
                else:
                    return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if user_obj != '':
                user = User_Profile.objects.get(user=user_obj)
                print(user)
                otp = {
                    "otp": generateOTP()
                }


                serializer = ResendOtpSerializer(user, data={"otp":otp['otp']}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    emailsending(otp, 'Activation_Email.html', user_obj, 'Email Confirmation')
                    return Response({'Message': 'Resend OTP Successfully!'}, status.HTTP_200_OK)
                else:
                    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


            else:
                return Response({'Message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        # {
        #     "otp": "9975"
        # }

        elif request.method == "POST":  # Check OTP and Activate Account
            try:

                user_obj = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                # print("***************")
                if "email" in request.data and User.objects.filter(username=request.data['email']).exists():
                    user_obj=User.objects.get(username=request.data['email'])
                else:
                    return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            otp_object = User_Profile.objects.get(user=user_obj)
            naive = otp_object.otp_time

            now_utc = datetime.now(timezone.utc)
            subtract_date = (now_utc - naive)
            minutes = (subtract_date.seconds // 60) % 60

            if minutes > 5:
                return Response({'Message': "OTP Expired! "}, status=status.HTTP_408_REQUEST_TIMEOUT)
            otp=request.data['otp']
            if otp==otp_object.otp:
                serializer = ResendOtpSerializer(otp_object, data={"verfication_status": True}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'Message': "Account Verified!"}, status=status.HTTP_200_OK)
                else:
                    return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


            return Response({'Message': "Wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)
    #
    # {
    #     "phone_number": "03356105885",
    #     "password": "MMMirza@1213AAA"
    # }

    @action(detail=False, methods=['post', 'put'])
    def signup_phone(self, request):  # user_login
        if request.method == "POST":
            if User.objects.filter(Q(username=request.data['phone_number'])).exists():
                return Response({"msg": "Already Registered"}, status.HTTP_306_RESERVED)
            else:
                if password_strenght(request.data['password']) > 0.25:
                    user = User.objects.create_user(username=request.data['phone_number'],
                                                    password=request.data['password'])
                    if user != '':
                        phone = request.data['phone_number']
                        user = User.objects.get(username=phone)


                        serializer = ProfilePostUserSerializer(data={"user": user.id,"registration_status":False})
                        if serializer.is_valid():
                            serializer.save()
                            twilio_otp(request.data['phone_number'])
                            return Response({'Message': 'Successfully'}, status.HTTP_200_OK)
                        else:
                            print(serializer.errors)
                            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
                return Response({"Message": "Weak password"}, status=status.HTTP_411_LENGTH_REQUIRED)
        if request.method=="PUT":# Update User profile
            try:
                user_obj = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                return Response({"Message":"User does not exist"},status=status.HTTP_404_NOT_FOUND)


            profile_obj = request.data
            serializer = ProfilePostSerializer(user_obj,data=profile_obj,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Update Profile Successfully!'}, status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=['post', 'put'])
    def twilio_otp(self, request):  # user_login
        if request.method == "POST":  # verify OTP
            try:
                user_obj = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                if "email" in request.data and User.objects.filter(username=request.data['email']).exists():
                    user_obj = User.objects.get(username=request.data['email'])
                else:
                    return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
            otp_object = User_Profile.objects.get(user=user_obj)
            sender_phone=user_obj.username
            otp = request.data['otp']
            if otp_verification_check(sender_phone,otp)==True:
                serializer = ResendOtpSerializer(otp_object, data={"verfication_status": True}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'Message': "Account Verified!"}, status=status.HTTP_200_OK)
                else:
                    return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'Message': "OTP Expired!"}, status=status.HTTP_400_BAD_REQUEST)


        if request.method == "PUT":# Resend OTP
            try:
                user_obj = User.objects.get(id=request.user.id)
            except User.DoesNotExist:
                if "email" in request.data and User.objects.filter(username=request.data['email']).exists():
                    user_obj = User.objects.get(username=request.data['email'])
                else:
                    return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            if user_obj != '':
                user = User_Profile.objects.get(user=user_obj)
                send_number=user.user.username
                twilio_otp(send_number)
                return Response({'Message': 'Resend OTP Successfully!'}, status.HTTP_200_OK)
            else:
                return Response({'Message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class password(viewsets.ViewSet):#User class
    @action(detail=False, methods=['post'])
    def forget_password(self,request):#forget pass email
        email=request.data['email']
        temp =isNum(email)
        if temp == False:
            if (User.objects.filter(username=email).exists()):
                user=User.objects.get(username=email)

                # pro=User_Profile.objects.get(user__id=user.id)
                # pro.forget_password_key=secret_id
                # pro.save()

                user = User_Profile.objects.get(user=user)
                # print(user)
                if user != '':
                    otp = {
                        "otp": generateOTP()
                    }
                    serializer = ResendOtpSerializer(user, data={"otp": otp['otp']}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        emailsending(otp, 'Activation_Email.html', user, 'Email Confirmation')
                        return Response({'Message': 'OTP Send Successfully!'}, status.HTTP_200_OK)
                    else:
                        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'Message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"msg": "Not valid Email"}, status.HTTP_404_NOT_FOUND)
        if temp == True:
            if (User.objects.filter(username=email).exists()):
                user=User.objects.get(username=email)
                twilio_otp(user)
                return Response({'Message': 'OTP Send Successfully!'}, status.HTTP_200_OK)
            else:
                return Response({"msg": "Number is not Register"}, status.HTTP_404_NOT_FOUND)
    # @action(detail=False, methods=['put', 'post'])
    # def otp_verification(self, request):
    #     print(request.user)
    #     if request.method == "PUT":  # Resend OTP
    #         try:
    #             user_obj = User.objects.get(id=request.user.id)
    #         except User.DoesNotExist:
    #             return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    #
    #         if user_obj != '':
    #             user = User_Profile.objects.get(user=user_obj)
    #             print(user)
    #             otp = {
    #                 "otp": generateOTP()
    #             }
    #         serializer = ResendOtpSerializer(user, data={"otp": otp['otp']}, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             emailsending(otp, 'Activation_Email.html', user_obj, 'Email Confirmation')
    #             return Response({'Message': 'OTP Resend Successfully!'}, status.HTTP_200_OK)
    #         else:
    #             return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #         # {
    #         #     "otp": "9975"
    #         # }
    #
    #     if request.method == "POST":  # Check OTP and Activate Account
    #         user_obj = User.objects.get(id=request.user.id)
    #         otp_object = User_Profile.objects.get(user=user_obj)
    #         naive = otp_object.otp_time
    #
    #         now_utc = datetime.now(timezone.utc)
    #         subtract_date = (now_utc - naive)
    #         minutes = (subtract_date.seconds // 60) % 60
    #
    #         if minutes > 5:
    #             return Response({'Message': "OTP Expired! "}, status=status.HTTP_408_REQUEST_TIMEOUT)
    #         otp = request.data['otp']
    #         if otp == otp_object.otp:
    #             serializer = ResendOtpSerializer(otp_object, data={"verfication_status": True}, partial=True)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 return Response({'Message': "Email Verified!"}, status=status.HTTP_200_OK)
    #             else:
    #                 return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    #
    #         return Response({'Message': "Wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)
    #
    # {
    #     "email": "muhammad.ehsan@argonteq.com",
    #     "password1": "pakistan0sadasAAA@@@001",
    #     "password2": "pakistan0sadasAAA@@@001"
    #
    # }
    # {
    #     "email": "jaryzaro@onekisspresave.com",
    #     "password": "hhbbwpongnk"
    # }

    @action(detail=False, methods=['put'])
    def reset_password(self, request):

        print(User_Profile.objects.all())

        password1 = request.data['password1']
        password2 = request.data['password2']
        if password1 == password2:
            password = password2

            if password_strenght(password) > 0.25:
                # user = User.objects.create_user(
                #     username=request.data['email'],
                #     password=request.data['password']
                #
                # )
                user_obj = User.objects.get(username=request.data['email'])
                change_pass = User.objects.get(pk=user_obj.id)
                change_pass.set_password(password)
                change_pass.save()
                print("/////////////////******************////////////////////")

                # print("user_obj")
                # passwordf =user_obj.set_password(password)
                # print(passwordf)
                # user_obj = User.objects.get(id=request.user.id)
                # profile_obj = request.data
                return Response({'Message': 'Successfully update'}, status.HTTP_200_OK)

            return Response({"Message": "Weak password"}, status=status.HTTP_411_LENGTH_REQUIRED)
        else:
            return Response({'Message': 'password_mismatch'}, status=status.HTTP_400_BAD_REQUEST)

# {
# "accessToken":"ya29.a0ARrdaM-kYCJLMritOsQ6SnNY0lyN2Kf1EQRYtUuaGmX…6sm0JrNDhTnXAgMy4fXeEtAXPJMnjxgP7W1HgOHYbesYtS0C5",
# "provider" : "google"
# }
# class sociallogin(APIView):
#     def post(self, request):
#         try:
#             dic = request.data
#             socialAuthToken = dic["accessToken"]
#             image = ''
#
#             if "photoUrl" in dic:
#                 image = dic["photoUrl"]
#
#                 print(socialAuthToken)
#                 # print("Facebook")
#
#             headers = {
#                 'Authorization': 'Bearer {0}'.format(socialAuthToken),
#                 "Content-Type": "application/json"}
#
#             def Facebook():
#                 social_verification = requests.post("https://graph.facebook.com/v2.8/me", headers=headers)
#                 print(social_verification)
#                 return social_verification.status_code == 200
#
#             def Google(token):
#                 print("token", token)
#                 social_verification = requests.get(
#                     "https://www.googleapis.com/oauth2/v2/tokeninfo?access_token={0}".format(token))
#                 print("Check", social_verification)
#
#                 return social_verification.status_code == 200
#
#             # if (dic["provider"] == "FACEBOOK") or (dic["provider"] == "facebook"):
#             #     is_valid = Facebook()
#             # el
#             if (dic["provider"] == "google") or (dic["provider"] == "GOOGLE"):
#                 is_valid = Google(socialAuthToken)
#             else:
#                 return Response({"msg": ("Provided information is not valid")}, status=status.HTTP_409_CONFLICT)
#
#             print(is_valid)
#             profile = ''
#             if is_valid:
#
#                 """if (email_verifying(request.data['email'])):
#                     return generate_email_error()
#
#                 if (username_verifying(request.data['username'])):
#                     return generate_username_error()
#                 """
#                 password = "{0}{1}{2}".format(dic["provider"], dic["id"], "ciwac")
#
#                 if 'email' in dic and dic['email'] != None and dic['email'] != '':
#                     pass
#                 else:
#                     if "name" in dic and dic['name'] != "":
#                         email_name = dic['name'].replace(' ', '-')
#                         dic['email'] = email_name.lower() + dic['id'] + '@' + dic['provider'] + '.com'
#                     else:
#                         dic['email'] = dic['provider'] + dic['id'] + '@' + dic['provider'] + '.com'
#                 if User.objects.filter(username=dic['email']).exists():
#                     print("in if")
#                     object_user = User.objects.get(username=dic['email'])
#                     user = PersonalInfo.objects.get(user=object_user)
#                     if "name" in dic and dic['name'] != "":
#                         name = dic['name']
#                         name = name.split(' ')
#                         object_user.first_name = name[0]
#                         object_user.last_name = name[1]
#                         object_user.save()
#                     print('image')
#                     print(image)
#                     if image:
#                         user.user_profile_image = image
#                         user.save()
#
#
#                 else:
#                     print('innnn')
#                     # username = dic["name"]
#
#                     try:
#                         build = request.headers['Build-Version']
#                     except:
#                         build = 'global'
#                     try:
#                         language = request.headers['accept-language']
#                     except:
#                         language = 'en'
#
#                     object_user = User(username=dic['email'], email=dic['email'])
#                     if "name" in dic and dic['name'] != "":
#                         name = dic['name']
#                         name = name.split(' ')
#                         object_user.first_name = name[0]
#                         object_user.last_name = name[1]
#                     object_user.is_active = True
#                     object_user.set_password(raw_password=password)
#                     object_user.save()
#                     persoanlInfo = PersonalInfo(user=object_user, email=object_user.email, user_profile_image=image)
#                     persoanlInfo.save()
#                     try:
#                         employee = EmployeeProfile(user=persoanlInfo)
#                         employee.user_language = language
#                         try:
#                             employee.registered_from = build
#                         except:
#                             pass
#                         employee.save()
#                     except:
#                         pass
#                     # persoanlInfo.save()
#
#                     object_user.set_password(password)
#                     object_user.save()
#
#                 try:
#                     token = get_jwt_token(object_user)
#                     # login(request, user)
#                     request.session["username"] = object_user.username
#                     # request.session.set_expiry(20)
#                     employee = EmployeeProfile.objects.get(user__user=object_user)
#                     empserializer = EmployeeProfileCompleteBusinessInformationSerializer(employee).data
#
#                     # try:
#                     #     fcm = PUSHToken.objects.create(user=employee, device_id=request.data['push_token'])
#                     #     fcm.save()
#                     # except:
#                     #     pass
#                     return Response(
#                         {"token": token, "emp_info": empserializer},
#                         status=status.HTTP_200_OK)
#                 except Exception as e:
#                     return Response({"msg": ("Something went wrong!"), "Error": str(e)},
#                                     status=status.HTTP_409_CONFLICT)
#
#             return Response({"msg": ("Problem in Social Login!")},
#                             status=status.HTTP_409_CONFLICT)
#         except Exception as e:
#             return Response({"msg": ("Something went wrong!"), "Error": str(e)}, status=status.HTTP_409_CONFLICT)
# # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxODAsInVzZXJuYW1lIjoiZmFyYXoubWlyemFAYXJnb250ZXEuY29tIiwiZXhwIjoxNjI1NjY1OTcwLCJlbWFpbCI6IiJ9._Z4UpJ5olhpVoow_cw7cxrx39inTAu3kA37hf7T_dp8
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImZhcmF6Lm1pcnphQGFyZ29udGVxLmNvbSIsImV4cCI6MTYyNTcyNjY3NywiZW1haWwiOiIifQ.A9-eOwQhZ9HWIpTcV5u1SMFPEFHjWFDrSuSvRm8USzo
# @login_required(login_url='/blog/login/')
class homescreen(viewsets.ViewSet):#Homescreen class
    @action(detail=False, methods=['get'])
    def homescreen_profile(self,request):
        try:
            user_obj = User_Profile.objects.get(user=request.user)
        except User.DoesNotExist:
            return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        # print(user_obj)
        # print("===============================")
        if user_obj != '':
            interested = user_obj.interested_in
            city = user_obj.city
            # user =User.objects.get(id=request.user.id)
            # print(user)
            # created_date= user_obj.created_date
            # print(created_date)
            # naive = user_obj.created_date
            # now_utc = datetime.now(timezone.utc)
            # print(type(naive))
            # print(naive)
            # print("==================")
            # print(now_utc)
            # print(type(now_utc))
            # subtract_date = (now_utc - naive)
            # minutes = (subtract_date.seconds // 60) % 60
            # gender = interested,city=city
            all_object = User_Profile.objects.filter(gender = interested,city=city)
            all = all_object.exclude(user=self.request.user)
            # print(all,"++++++++++++++++++++++===")
            serializer = ProfileScreenSerializer(all, many=True)
            return Response({"All Profiles": serializer.data})
        return Response({"msg": "Home Screen"}, status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def homescreen_filters(self, request):
        try:
            user_obj = User_Profile.objects.get(user=request.user)
        except User.DoesNotExist:
            return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if user_obj !='':
            # height= request.data['height']
            # education= request.data['education']
            # kids= request.data['kids']
            # drink= request.data['drink']
            # smoke= request.data['smoke']
            # city= request.data.get('city', None)['city']
            # age= request.data['age']
            # exercise= request.data['exercise']
            # religion= request.data['religion']
            # gender = interested,city=city
            # list = {
            #     "kids": "Y",
            #     "religion": "Christian",
            #     "age": "21",
            # }
            # print(list)
            # print("===================")
            height = request.GET.get('height')
            education = request.GET.get('education')
            kids = request.GET.get('kids')
            drink = request.GET.get('drink')
            smoke = request.GET.get('smoke')
            city = request.GET.get('city')
            age = request.GET.get('age')
            exercise = request.GET.get('exercise')
            religion = request.GET.get('religion')

            list= {}
            set_if_not_none(list, 'height', height)
            set_if_not_none(list, 'education', education)
            set_if_not_none(list, 'kids', kids)
            set_if_not_none(list, 'drink', drink)
            set_if_not_none(list, 'smoke', smoke)
            set_if_not_none(list, 'city', city)
            set_if_not_none(list, 'age', age)
            set_if_not_none(list, 'exercise', exercise)
            set_if_not_none(list, 'religion', religion)
            #
            # print(list)
            # print("====================================")
            # all_object = User_Profile.objects.filter(**list)


            page = Pagination(request, 5)
            all_profile = page.advance_filter_pagination("User_Profile",list)


            serializer = ProfileScreenSerializer(all_profile, many=True)
            return Response({"AllProfiles": serializer.data})


class like_and_dislike(viewsets.ViewSet):#like and dislike class
    @action(detail=False, methods=['post'])
    def like_dislike(self,request):
        try:
            #       user_obj = User.objects.get(id=request.user.id)
            user_obj = User_Profile.objects.get(user=request.user)
        except User.DoesNotExist:
            return Response({"Message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        data=qdict_to_dict(request.data)
        data['user']=user_obj.id
        print(data)
        serializer = LikeDislikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({'Message': 'Update Profile Successfully!'}, status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
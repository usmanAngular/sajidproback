import math, random
import random

from core import models
import random

from core import models

import core


def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be chaged
    # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60


def twilio_otp(number):
    # (843)256 - 4013
    # +18432564013
    account_sid = 'AC2313b9e0e569700f787f2ab1aac72d0b'
    auth_token = 'ce6828112a78ef13a6bd9b665850a321'
    client = Client(account_sid, auth_token)
    verification = client.verify \
        .services('VA79e9c5e566a341bee03add8cc5d63e37') \
        .verifications \
        .create(to='+92'+str(number), channel='sms',)

    print(verification)

def otp_verification_check(number,otp_code):


    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC2313b9e0e569700f787f2ab1aac72d0b'
    auth_token =  'ce6828112a78ef13a6bd9b665850a321'
    client = Client(account_sid, auth_token)

    try:
        verification_check = client.verify.services('VA79e9c5e566a341bee03add8cc5d63e37')\
            .verification_checks.create(to='+92'+str(number), code=otp_code)
        return True
    except:
        return False
    # print(verification_check.valid)
    # if verification_check.valid=="True":
    #     return True
    # else:
    #     return False



class Pagination:
    def __init__(self,request, num_of_records):
        self.request = request
        self.num_of_records = num_of_records


    # instance method
    def custom_pagination(self, objects, model_name):
        try:
            page = int(self.request.GET.get('page'))
            if page < 1:
                page = 1
        except:
            page = 1
        items = page * self.num_of_records
        offset = (page - 1) * self.num_of_records
        all_seller_lead = model_name.objects.filter(user=self.request.user).order_by("id")[offset:items]
        totalitems = int(model_name.objects.count())
        totalpages = int(totalitems / self.num_of_records)
        per = totalitems % self.num_of_records
        if per != 0:
            totalpages += 1
        return all_seller_lead

    def advance_filter_pagination(self,model_name,list):
        try:
            page = int(self.request.GET.get('page'))
            if page < 1:
                page = 1
        except:
            page = 1
        items = page * self.num_of_records
        offset = (page - 1) * self.num_of_records
        model = getattr(core.models, model_name)
        print(list)
        all_object = model.objects.filter(**list)
        # print(all_object,"++++++++++++++++++++++++++")
        all_profile = all_object.exclude(user=self.request.user).order_by("id")[offset:items]
        # print(self.request.user,"UUUUUUUUUUUUUUSER")
        lenght = len(all_profile)
        # print(lenght,"=========================")
        # totalitems = int(model.objects.count())
        totalpages = int(lenght / self.num_of_records)
        per = lenght % self.num_of_records
        if per != 0:
            totalpages += 1
        return all_profile



        # serializer = serializer_name(all_seller_lead, many=True)
        # return Response(serializer.data)

def qdict_to_dict(qdict):
    """Convert a Django QueryDict to a Python dict.

    Single-value fields are put in directly, and for multi-value fields, a list
    of all values is stored at the field's key.

    """
    return {k: v[0] if len(v) == 1 else v for k, v in qdict.lists()}
from django.conf.urls import url, include
from django.urls import path,include
# from django.urls import
# from .views import *
from django.views.generic import TemplateView

from . import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token,verify_jwt_token
from .views import *



router=routers.DefaultRouter()
router.register(r'order', Order_Class, 'Order')#Place order

# router.register(r'like_and_dislike', FRAZ, 'like_and_dislike')
urlpatterns=[
    path('', include(router.urls)),


]
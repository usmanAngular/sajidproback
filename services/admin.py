from django.contrib import admin

# Register your models here.
from services.models import Order,Services_Type,Services_Level,Paper_type,Pricing,Coupen

admin.site.register(Order)
admin.site.register(Services_Type)
admin.site.register(Services_Level)
admin.site.register(Paper_type)
admin.site.register(Pricing)
admin.site.register(Coupen)
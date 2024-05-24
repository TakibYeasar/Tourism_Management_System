# admins.py
from django.contrib import admin
from .models import *

admin.site.register(TourPackage)
admin.site.register(Booking)
admin.site.register(Guide)

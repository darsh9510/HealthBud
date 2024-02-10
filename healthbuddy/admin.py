from django.contrib import admin

from .models import Massage,Disease,Rooms,Doctor

admin.site.register(Massage)
admin.site.register(Disease)
admin.site.register(Rooms)
admin.site.register(Doctor)

from django.contrib import admin

from .models import Realization, Appointment, Message


admin.site.register(Appointment)
admin.site.register(Message)
"""
admin.site.register(Comments)
"""
admin.site.register(Realization)

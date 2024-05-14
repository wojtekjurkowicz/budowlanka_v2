from django.contrib import admin

from .models import Realization, Appointment, Message, Comment


admin.site.register(Appointment)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Realization)

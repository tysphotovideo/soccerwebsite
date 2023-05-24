from django.contrib import admin
from .models import  Contact, Event, Tickets

# Register your models here.

admin.site.register(Event)
admin.site.register(Tickets)
admin.site.register(Contact)


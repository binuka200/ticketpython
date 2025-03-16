from django.contrib import admin

# Register your models here.

from .models import Status, Ticket, TicketPost, TicketType, Department

admin.site.register(Status)
admin.site.register(Ticket)
admin.site.register(TicketPost)
admin.site.register(TicketType)
admin.site.register(Department)
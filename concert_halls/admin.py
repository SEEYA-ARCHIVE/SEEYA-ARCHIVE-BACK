from django.contrib import admin
from .models import ConcertHall, Floor, Seat

admin.site.register(ConcertHall)
admin.site.register(Floor)
admin.site.register(Seat)
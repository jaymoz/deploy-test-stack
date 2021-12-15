from django.contrib import admin
from .models import Bookings,Parking_Space

admin.site.index_title = "Fregat office center"
admin.site.site_header = "Fregat office center Admin"
admin.site.register(Bookings)
admin.site.register(Parking_Space)
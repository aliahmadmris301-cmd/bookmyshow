from django.contrib import admin
from .models import Event, Booking
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=(
        'title',
        'date',
        'venue',
        'price',
        'available_seats'
    )
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=(
        'user',
        'event',
        'booking_date',
        'quantity'
    )
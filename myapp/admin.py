from django.contrib import admin
from django.conf import settings  # Import Django settings module
from .utils import send_sms
from django import forms
import logging
from .models import *


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_name','price','Luggage','Seats')

# admin.site.register(Car)

@admin.register(message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'tellme')

@admin.register(RegisterData)
class RegisterDataAdmin(admin.ModelAdmin):
    list_display = ('username', 'age', 'contact', 'email', 'address')

@admin.register(LoginData)
class LogindataAdmin(admin.ModelAdmin):
    list_display = ('username','password')


logger = logging.getLogger(__name__)

def send_sms(phone_number, message):
    try:
        from twilio.rest import Client
        account_sid = 'AC9a54847635c5e55d3dc802cb7439d3e0'
        auth_token = '80a776f2b9e85d34d42e3ccd97dfcd7d'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message,
            from_='+17632601932',
            to=phone_number
        )
        logger.info(f"SMS sent to {phone_number}: {message.sid}")
    except Exception as e:
        logger.error(f"Failed to send SMS to {phone_number}: {e}")

@admin.register(MyReserve)
class MyReserveAdmin(admin.ModelAdmin):
    list_display = ['Car', 'name', 'email', 'approved', 'declined']
    actions = ['approve_reservations', 'decline_reservations']

    def approve_reservations(self, request, queryset):
        for reservation in queryset:
            reservation.approve_reservation()
            # Send SMS notification to the user
            send_sms(reservation.phone_number, f'Your reservation for {reservation.Car}has been approved. Thank you for choosing us.')
        self.message_user(request, "Selected reservations have been approved and notifications sent.")

    approve_reservations.short_description = "Approve selected reservations"

    def decline_reservations(self, request, queryset):
        for reservation in queryset:
            reservation.decline_reservation()
            # Send SMS notification to the user
            send_sms(reservation.phone_number, f'We regret to inform you that your reservation for {reservation.Car} has been declined.')
        self.message_user(request, "Selected reservations have been declined and notifications sent.")

    decline_reservations.short_description = "Decline selected reservations"

    # admin.site.register(MyReserve,MyReserveAdmin)


# Register your models here.

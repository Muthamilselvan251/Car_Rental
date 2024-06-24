from django.db import models
from django.core.exceptions import ValidationError
from twilio.rest import Client
from django.conf import settings
from django.utils import timezone
import datetime
from django import forms
import os
import re


def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class Car(models.Model):
    car_name = models.CharField(max_length=150,null=True,blank=True)
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    additional_image1 = models.ImageField(upload_to='additional_cars/', blank=True, null=True)
    additional_image2 = models.ImageField(upload_to='additional_cars/', blank=True, null=True)
    additional_image3 = models.ImageField(upload_to='additional_cars/', blank=True, null=True)
    price = models.IntegerField(default="")
    kilometer = models.CharField(max_length=150,null=True,blank=True)
    Luggage = models.CharField(max_length=150)
    Seats = models.CharField(max_length=150)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden")

    class Meta:
        db_table = 'Car'

    def __str__(self):
        return self.car_name


def negative(value):
    if value <= 0:
        raise ValidationError('Age cannot be negative.')
    elif value < 18:
        raise ValidationError('You are age  under 18 so not eligible for this site.')
    elif len(str(value)) > 2:
        raise ValidationError('Age must be two number.')

def number(number):
    if len(str(number)) < 10:
        raise ValidationError('contact number less then 10 numbers.')
    elif len(str(number)) > 10:
        raise ValidationError('contact number greater than 10 numbers.')

def validate_email(value):
    if not re.match(r'^[^@]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}$', value):
        raise ValidationError(
            'Invalid email format. Please provide a valid email address.'
        )

class RegisterData(models.Model):
    username = models.CharField(max_length=50,null=False,blank=False)
    age = models.IntegerField(default="",validators=[negative])
    contact = models.BigIntegerField(primary_key=True,validators=[number])
    email = models.EmailField(max_length=50,default="",validators=[validate_email])
    address = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=20, default="")
    confirm_password = models.CharField(max_length=20, default="")
    # token = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table ='Registerform'

    def __str__(self):
        return self.username

class MyPassword(models.Model):
    user = models.ForeignKey(RegisterData, on_delete=models.CASCADE)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'password_history'

    def __str__(self):
        return f"Password history for {self.user.username}"

class LoginData(models.Model):
    username = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=50, default="")

    class Meta:
        db_table = 'Loginform'

    def __str__(self):
        return self.username

class message(models.Model):
    fullname = models.CharField(max_length=50,null=False,blank=False)
    email = models.EmailField(max_length=50,default="",validators=[validate_email])
    tellme = models.CharField(max_length=250,null=False,blank=False)

    class Meta:
        db_table = "Usermessage"

    def __str__(self):
        return self.fullname



class MyReserve(models.Model):
    Car = models.CharField(max_length=150, null=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = models.CharField(max_length=150, default="")
    age = models.IntegerField(default="", validators=[negative])
    phone_number = models.BigIntegerField(validators=[number])
    email = models.EmailField(max_length=50, default="", validators=[validate_email])
    pickup = models.CharField(max_length=20, default="")
    dropoff = models.CharField(max_length=20, default="")
    pickdate = models.DateField(default=timezone.now)
    dropdate = models.DateField()
    picktime = models.TimeField(default=None, blank=True, null=True)
    droptime = models.TimeField(default=None, blank=True, null=True)
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'MyReserve'

    def __str__(self):
        return self.Car

    def clean(self):
        super().clean()

        if self.dropdate < self.pickdate:
            raise ValidationError({'dropdate': ('Drop date should be after pick date.')})

        if self.pickdate < timezone.now().date():
            raise ValidationError('Pick date must be in the future.')


    def approve_reservation(self):
        self.approved = True
        self.declined = False
        self.save()

        car_name = self.Car
        car_price = self.price

        message = f"Your reservation for '{car_name}' with price '{car_price}' has been approved. Thank you for choosing us! If you have any questions, please contact us."
        self.send_notification(message)

    def decline_reservation(self):
        self.declined = True
        self.approved = False
        self.save()

        message = "Your reservation has been declined. Please contact us if you have any questions."
        self.send_notification(message)

    def send_notification(self, message):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        try:
            message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to='+918220954353'  # Update with recipient's phone number
            )
            print("SMS sent successfully with SID:", message.sid)
            return True
        except Exception as e:
            print("Failed to send SMS:", e)
            return False

    def calculate_total_price(self):
        days_difference = (self.dropdate - self.pickdate).days
        return self.price * days_difference

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform full model validation, including clean() method
        super().save(*args, **kwargs)

# class Payment(models.Model):
#     order_id = models.CharField(max_length=100)
#     payment_id = models.CharField(max_length=100)
#     signature = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=100, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = "Payment"
#
#     def __str__(self):
#         return self.order_id
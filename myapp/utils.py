# utils.py
from twilio.rest import Client
from django.conf import settings


def send_sms(phone_number, message):
    # phone_number = '+918220954353'
    # message = 'Your reservation has been approved. Thank you!'

    try:

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send SMS message
        response = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        print("SMS sent successfully with SID:", response.sid)
        return True  # Return True to indicate success
    except Exception as e:
        # Log the error or handle it appropriately
        print("Failed to send SMS:", e)
        return False  # Return False to indicate failure

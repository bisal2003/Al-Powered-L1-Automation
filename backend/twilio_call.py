import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def make_call(phone_number):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

    call = client.calls.create(
        url=f"{os.getenv('NGROK_URL')}/voice",
        to=phone_number,
        from_=os.getenv("TWILIO_PHONE_NUMBER")
    )
    return call.sid

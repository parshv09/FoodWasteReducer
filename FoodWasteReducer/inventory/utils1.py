#dedicated for SMS alerts but not implemented DLT registration
'''

import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("FAST2SMS_API_KEY")


def format_number(number):
    number = str(number)
    if number.startswith("+"):
        return number
    elif number.startswith("0"):
        return "+91" + number[1:]
    elif number.startswith("91"):
        return "+" + number
    elif len(number) == 10:
        return "+91" + number
    else:
        raise ValueError(f"Invalid phone number format: {number}")


def send_sms(phone_number, message):
    url = "https://www.fast2sms.com/dev/bulkV2"
    
    payload = {
        "authorization": api_key,   # replace with your API key

        "message": message,
        "language": "english",
        "route": "q",          # For transactional route
        "numbers": "9922803115",
    }

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()

'''
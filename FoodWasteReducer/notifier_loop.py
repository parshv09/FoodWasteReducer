# notifier_loop.py
import time
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoodWasteReducer.settings')
django.setup()

from inventory.utils import send_expiry_notifications

while True:
    print("Checking for expiring items...")
    send_expiry_notifications()
    print("Emails sent. Sleeping for 24 hours.")
    time.sleep(24*60*60)  # sleep for 1 day (24 * 60 * 60)

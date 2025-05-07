from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from collections import defaultdict
from .models import FoodItems  # Adjust to match your model

def send_expiry_notifications():
    today = now().date()
    upcoming = today + timedelta(days=7)

    # Get items expiring in the next 7 days or already expired
    items = FoodItems.objects.filter(expiry_date__lte=upcoming)

    # Group items by user email
    user_items = defaultdict(list)
    for item in items:
        user_items[item.user.email].append(item)

    for email, user_food_items in user_items.items():
        expired = []
        urgent = []
        upcoming_list = []

        for item in user_food_items:
            days_left = (item.expiry_date - today).days
            formatted_date = item.expiry_date.strftime('%d-%m-%Y')
            line = f"- {item.name} — "

            if item.expiry_date < today:
                expired.append(line + f"expired on {formatted_date}")
            elif days_left <= 4:
                urgency = "tomorrow" if days_left == 1 else f"in {days_left} days"
                urgent.append(line + f"expiring {urgency} (on {formatted_date})")
            else:
                upcoming_list.append(line + f"expiring in {days_left} days (on {formatted_date})")

        # Construct email content
        message_lines = [
            "Hi,\n",
            "This is a friendly reminder about the food items in your inventory that are expiring soon or have already expired.\n",
            "Here’s a summary of what needs your attention:\n"
        ]

        if expired:
            message_lines.append("🔴 EXPIRED ITEMS:\nThese items have already passed their expiry date. Please discard them safely:")
            message_lines.extend(expired)
            message_lines.append("")

        if urgent:
            message_lines.append("🟠 EXPIRING VERY SOON (in 4 days or less):\nUse these soon to avoid waste:")
            message_lines.extend(urgent)
            message_lines.append("")

        if upcoming_list:
            message_lines.append("🟡 Upcoming Expiries (within 7 days):\nPlan to use these before they expire:")
            message_lines.extend(upcoming_list)
            message_lines.append("")

        message_lines.append("✅ Take action now to reduce food waste and stay safe.\n\nBest regards,\nfood Inventory Management System(FWRS)")

        full_message = "\n".join(message_lines)

        # Send the email
        send_mail(
            subject="🍽️ Food Expiry Alert – Items That Need Your Attention",
            message=full_message,
            from_email='develoer22@gmail.com',  # Replace with your real email
            recipient_list=[email],
            fail_silently=False,
        )

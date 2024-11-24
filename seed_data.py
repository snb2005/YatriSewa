import os
import django
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Accommodation, Booking

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  # Replace with your project name
django.setup()

from django.contrib.auth.models import User
from accounts.models import Accommodation, Booking

def create_seed_data():
    user = User.objects.get(username='testuser')  # Adjust as necessary
    accommodation = Accommodation.objects.create(
        name='Sample Hotel',
        location='Sample City',
        price=100.00,
        availability=True
    )
    Booking.objects.create(
        user=user,
        accommodation=accommodation,
        checkin_date=timezone.now().date(),
        checkout_date=timezone.now().date() + timezone.timedelta(days=2),
        guests=2
    )
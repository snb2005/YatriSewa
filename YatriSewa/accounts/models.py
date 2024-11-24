from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user:
            self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    availability = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    guests = models.IntegerField(default=1)

    def clean(self):
        if self.checkin_date >= self.checkout_date:
            raise ValidationError("Check-out date must be after check-in date.")

    def __str__(self):
        return f"{self.user.username} - {self.accommodation.name} ({self.checkin_date} to {self.checkout_date})"

class EmergencyContact(models.Model):
    service_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    category = models.CharField(max_length=50, choices=[('medical', 'Medical'), ('police', 'Police'), ('fire', 'Fire Brigade'), ('other', 'Other')])

    def __str__(self):
        return self.service_name
    
class SOSRequest(models.Model):
    user_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOS from {self.user_name} at {self.location}"
    
    
class EmergencyAnnouncement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    # Lost and Found Model
class LostAndFound(models.Model):
    LOST = 'L'
    FOUND = 'F'
    STATUS_CHOICES = [
        (LOST, 'Lost'),
        (FOUND, 'Found'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=LOST,
    )
    contact_info = models.CharField(max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    


from django.contrib import admin
from .models import Profile
from .models import Accommodation
from .models import EmergencyAnnouncement

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'email')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Accommodation)
admin.site.register(EmergencyAnnouncement)

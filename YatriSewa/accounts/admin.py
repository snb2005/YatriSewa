from django.contrib import admin
from .models import Profile
from .models import Accommodation
from .models import EmergencyAnnouncement
from .models import SOSRequest
from .models import LostAndFound

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address', 'email')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Accommodation)
admin.site.register(EmergencyAnnouncement)

admin.site.register(SOSRequest)

# Register LostAndFound model with admin
class LostAndFoundAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date_posted')
    list_filter = ('status', 'date_posted')
    search_fields = ('title', 'description')

admin.site.register(LostAndFound, LostAndFoundAdmin)



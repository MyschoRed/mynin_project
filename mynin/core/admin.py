from django.contrib import admin
from .models import Invitation, Teamleader, UserProfile, ProfileStatus, Settings


admin.site.register(ProfileStatus)
admin.site.register(UserProfile)
admin.site.register(Invitation)
admin.site.register(Teamleader)
admin.site.register(Settings)



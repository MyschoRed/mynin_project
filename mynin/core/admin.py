from django.contrib import admin
from .models import User, Invitation, Teamleader, UserProfile, ProfileStatus

admin.site.register(User)
admin.site.register(ProfileStatus)
admin.site.register(UserProfile)
admin.site.register(Invitation)
admin.site.register(Teamleader)

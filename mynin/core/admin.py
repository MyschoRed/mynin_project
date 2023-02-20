from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomCreateUserForm, CustomUserChangeForm
from .models import Invitation, UserProfile, ProfileStatus, Settings, CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomCreateUserForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'first_name',
        'last_name',
        'mobile',
        'address',
        'city',
        'postal_code']

    def address(self, obj):
        return obj.profile.address

    address.admin_order_field = 'profile__address'
    address.short_description = 'Address'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProfileStatus)
admin.site.register(UserProfile)
admin.site.register(Invitation)
# admin.site.register(Teamleader)
admin.site.register(Settings)

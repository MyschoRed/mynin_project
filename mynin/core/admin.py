from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomCreateUserForm, CustomUserChangeForm
from .models import Invitation, UserProfile, ProfileStatus, Settings, CustomUser, Invoice


class CustomUserAdmin(UserAdmin):
    add_form = CustomCreateUserForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'first_name',
        'last_name',
        'has_profile',
        'is_email_verified',
        'is_superuser',
        'is_active',
        'is_staff'
    ]
    fieldsets = (
        ('Login', {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'address', 'city', 'mobile')}),
        ('Permissions', {'fields': ('has_profile', 'is_email_verified', 'is_staff', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'address')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProfileStatus)
admin.site.register(UserProfile)
admin.site.register(Invitation)
admin.site.register(Invoice)
admin.site.register(Settings)

from django.contrib import admin
from .models import User, Invitation, Member, Teamleader


admin.site.register(User)
admin.site.register(Invitation)
admin.site.register(Member)
admin.site.register(Teamleader)

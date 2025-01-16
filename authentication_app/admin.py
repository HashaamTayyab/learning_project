from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('contact_no', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('contact_no', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

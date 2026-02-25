from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Vehicle

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'phone')}),
    )

admin.site.register(Vehicle)

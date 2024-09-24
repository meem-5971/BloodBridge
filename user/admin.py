from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DonationHistory

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone', 'age', 'gender', 'blood_group', 'last_donation_date', 'is_active')
    search_fields = ('username', 'email', 'blood_group')
    readonly_fields = ('last_donation_date',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone', 'age', 'gender', 'blood_group', 'last_donation_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, UserAdmin)

class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ('donor', 'recipient', 'donation_date')
    search_fields = ('donor__username', 'recipient__username')

admin.site.register(DonationHistory, DonationHistoryAdmin)

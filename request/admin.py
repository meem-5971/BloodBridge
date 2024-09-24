from django.contrib import admin
from .models import BloodRequest

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'blood_group', 'created_at', 'accepted_by', 'status')
    search_fields = ('requester__username', 'blood_group', 'accepted_by__username')
    list_filter = ('status', 'blood_group', 'created_at')

admin.site.register(BloodRequest, BloodRequestAdmin)

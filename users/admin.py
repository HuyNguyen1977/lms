from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    ordering = ['-created_at']
    raw_id_fields = ['user']
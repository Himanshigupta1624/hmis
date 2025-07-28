from django.contrib import admin
from .models import Announcement, AnnouncementRead


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'audience', 'is_active', 'start_date', 'end_date', 'created_by']
    list_filter = ['priority', 'audience', 'is_active', 'start_date']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Announcement Details', {
            'fields': ('title', 'content', 'priority', 'audience')
        }),
        ('Visibility', {
            'fields': ('is_active', 'start_date', 'end_date')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(AnnouncementRead)
class AnnouncementReadAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'user', 'read_at']
    list_filter = ['read_at']
    search_fields = ['announcement__title', 'user__first_name', 'user__last_name']
    readonly_fields = ['read_at']

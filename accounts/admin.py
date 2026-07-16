from django.contrib import admin
from .models import UserProfile, UserUNEPermission


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'role_label', 'default_all_une_access')
    list_filter = ('role_label', 'default_all_une_access')
    search_fields = ('user__username', 'user__email', 'display_name', 'job_title')


@admin.register(UserUNEPermission)
class UserUNEPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'une', 'can_view_summary', 'can_view_detail', 'granted_by', 'granted_at')
    list_filter = ('une', 'can_view_summary', 'can_view_detail')
    search_fields = ('user__username', 'user__email', 'une__code', 'une__name_es')
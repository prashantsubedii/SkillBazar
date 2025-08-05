from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'rating', 'total_earnings', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('SkillBazar Profile', {
            'fields': ('user_type', 'bio', 'skills', 'profile_picture', 'banner_image', 
                      'phone_number', 'address', 'facebook_url', 'twitter_url', 
                      'linkedin_url', 'website_url', 'hourly_rate', 'total_earnings', 
                      'rating', 'total_reviews')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('SkillBazar Profile', {
            'fields': ('user_type', 'bio', 'skills', 'profile_picture', 'banner_image', 
                      'phone_number', 'address', 'facebook_url', 'twitter_url', 
                      'linkedin_url', 'website_url', 'hourly_rate')
        }),
    ) 
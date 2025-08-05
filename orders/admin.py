from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['gig', 'reviewer', 'freelancer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['gig__title', 'reviewer__username', 'freelancer__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at'] 
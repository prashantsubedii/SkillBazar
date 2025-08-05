from django.contrib import admin
from .models import Category, Gig, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ['title', 'freelancer', 'category', 'price', 'rating', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at', 'rating']
    search_fields = ['title', 'freelancer__username', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'rating', 'total_reviews']
    ordering = ['-created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'gig', 'buyer', 'freelancer', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['gig__title', 'buyer__username', 'freelancer__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at'] 
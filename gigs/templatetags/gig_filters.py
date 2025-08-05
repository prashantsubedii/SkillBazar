from django import template
from django.template.defaultfilters import title

register = template.Library()

@register.filter
def format_seller_name(user):
    """Format seller name with proper capitalization"""
    if user.get_full_name():
        return title(user.get_full_name())
    return title(user.username)

@register.filter
def format_price(price):
    """Format price with Nepali Rupee symbol"""
    return f"रु {price:,}"

@register.filter
def get_gig_image_url(gig):
    """Get gig image URL or placeholder"""
    if gig.image:
        return gig.image.url
    return f"https://via.placeholder.com/300x200/1877f2/ffffff?text={gig.title}" 
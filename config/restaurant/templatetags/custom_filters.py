from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def calculate_gst(value):
    """Calculate GST (18%) from the given value"""
    try:
        return Decimal(value) * Decimal('0.18')
    except (ValueError, TypeError):
        return Decimal('0.00') 
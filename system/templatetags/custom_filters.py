from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the value by the arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide the value by the arg"""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def calculate_duration(start_time, end_time):
    """Calculate duration between two times"""
    if not end_time:
        return "Đang đỗ"
    duration = end_time - start_time
    hours = int(duration.total_seconds() // 3600)
    minutes = int((duration.total_seconds() % 3600) // 60)
    return f"{hours} giờ {minutes} phút" 
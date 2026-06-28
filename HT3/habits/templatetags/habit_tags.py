import datetime
from django import template

register = template.Library()


@register.filter
def make_date(value):
    """Create a date from string parts: 'YYYY-MM-DD'"""
    try:
        parts = value.split('-')
        return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, AttributeError):
        return None


@register.filter
def get_entry(entries_dict, date_obj):
    """Get entry from dict by date object"""
    if entries_dict is None:
        return None
    return entries_dict.get(date_obj)

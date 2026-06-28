from django import template

register = template.Library()


@register.filter
def get_status_color(status):
    colors = {
        'todo': 'bg-yellow-100 text-yellow-700',
        'in_progress': 'bg-blue-100 text-blue-700',
        'done': 'bg-green-100 text-green-700',
    }
    return colors.get(status, 'bg-gray-100 text-gray-700')

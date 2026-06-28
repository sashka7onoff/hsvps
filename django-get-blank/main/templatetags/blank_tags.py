from django import template

register = template.Library()


@register.filter
def form_of_position(num):
    cases = [2, 0, 1, 1, 1, 2]
    titles = ['позиция', 'позиции', 'позиций']
    n = abs(num)
    if n % 100 > 4 and n % 100 < 20:
        index = 2
    else:
        index = cases[min(n % 10, 5)]
    return titles[index]


@register.filter
def multiply(value, arg):
    try:
        return round(float(value) * float(arg), 2)
    except (ValueError, TypeError):
        return 0

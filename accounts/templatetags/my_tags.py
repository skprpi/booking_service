from django import template

register = template.Library()


@register.filter
def get_item_by_idx(p, i):
    try:
        return p[i]
    except:
        return None


@register.filter
def get_index_from_table(a, b):
    try:
        return a * 4 + b
    except:
        return None


@register.filter
def get_minutes(a):
    try:
        return a * 15
    except:
        return None

register.filter('get_item_by_idx', get_item_by_idx)
register.filter('get_index_from_table', get_index_from_table)
register.filter('get_minutes', get_minutes)
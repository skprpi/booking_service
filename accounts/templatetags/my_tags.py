from django import template

register = template.Library()


@register.filter
def get_item_by_idx(p, i):
    try:
        return p[i]
    except:
        return None

register.filter('get_item_by_idx', get_item_by_idx)
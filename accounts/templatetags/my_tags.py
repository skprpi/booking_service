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

@register.filter
def get_collapse_name(a):
    try:
        s = ''
        for i in range(len(a)):
            s += 'collapse' + str(i + 1) + ' '
        s.rsplit(' ')
        return s
    except:
        return None

@register.filter
def make_zerofill(a):
    try:
        if int(a) < 10:
            return '0' + str(a)
        return a
    except:
        return None

register.filter('get_item_by_idx', get_item_by_idx)
register.filter('get_index_from_table', get_index_from_table)
register.filter('get_minutes', get_minutes)
register.filter('get_collapse_name', get_collapse_name)
register.filter('make_zerofill', make_zerofill)
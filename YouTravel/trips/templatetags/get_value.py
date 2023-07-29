from django import template

register = template.Library()


@register.filter(name='get_value')
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_comment')
def get_comment(comment_all, key):
    comments = comment_all.filter(trip_id=key)
    return comments

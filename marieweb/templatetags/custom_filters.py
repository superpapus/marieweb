from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if str(key) in dictionary:
        return dictionary[str(key)]
    return None
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def attr(obj, attr):

    try:
        result = obj[attr]
    except:
        return unicode()

    if type(result) == type(datetime.now()):
        return result.strftime('%d/%m/%Y')

    return result
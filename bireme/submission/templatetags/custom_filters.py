from django import template
import hashlib
from django.template.loader import get_template

register = template.Library()

@register.filter(name='md5')
def md5_string(value):
    value = str(value)
    return hashlib.md5(value).hexdigest()

@register.filter
def in_group(user, groups):
    group_list = unicode(groups).split(',')
    return bool(user.groups.filter(name__in=group_list).values('name'))

@register.filter(name='translate')
def translate(obj, lang):
    try:
        return obj.get_translation(lang)
    except:
        return obj

@register.filter(name='exists')
def exists(obj):
    try: 
        template = get_template(obj)
        return True
    except Exception as e:
        return False
    

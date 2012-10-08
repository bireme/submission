from django import template
import hashlib

register = template.Library()

#
# {{ "some identifier"|md5 }}
# g87g98ht02497hg349ugh3409h34
#
@register.filter(name='md5')
def md5_string(value):
    value = str(value)
    return hashlib.md5(value).hexdigest()

@register.filter
def in_group(user, groups):
    group_list = unicode(groups).split(',')
    return bool(user.groups.filter(name__in=group_list).values('name'))
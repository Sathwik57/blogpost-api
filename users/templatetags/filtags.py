from django import template
from django.template.defaultfilters import stringfilter

from users.models import Follow

register = template.Library()


@register.filter
def tag_filter(value):
    a = ' #'.join(x.name for x in value)
    return a

@register.simple_tag(takes_context=True)
def follow_finder(context , profile):
    folower = context['cur_user']
    print(profile,folower)
    try:
        Follow.objects.get(follower = folower , following = profile ) 
        return True
    except:
        return False
        
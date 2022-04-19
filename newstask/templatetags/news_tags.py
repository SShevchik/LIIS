from django import template
from django.db.models import Q

from newstask.models import Subscription

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='can_subscribe')
def can_subscribe(user, author_id):
    if user.id == author_id:
        return False
    if Subscription.objects.filter(Q(author_id=author_id) & Q(subscriber_id=user.id)):
        return False
    return True

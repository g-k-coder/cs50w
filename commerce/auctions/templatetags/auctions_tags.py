from django import template
from ..models import Watchlist


register = template.Library()

@register.simple_tag
def watch_items(user_id):
    items = Watchlist.objects.filter(user_id=user_id)
    
    if items:
        return len(items)
    else:
        return ''
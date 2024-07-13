from django import template
from reviews.models import Item

register = template.Library()

@register.filter(name='get_item_by_id')
def get_item_by_id(item_id):
    return Item.objects.get(pk=item_id)

from django import template
from chart.models import Order


register=template.Library()


@register.filter

def cart_item_count(user):
    if user.is_authenticated:
        qs=Order.objects.filter(user=user,Ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

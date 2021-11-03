import collections

from django.contrib.auth import get_user_model
from django.db.models import Count

from shop.models import Cake, Order


User = get_user_model()


def get_statistics():

    statistics = {
        'orders': {'Всего заказов': Order.objects.count()},
        'statuses': dict(collections.Counter(
            order.get_status_display() for order in Order.objects.only('status')
            )
        ),
        'clients': {'Всего клиентов': User.objects.filter(is_staff=False).count()},
        'topping': dict(
            Cake.objects.values_list('topping__name').annotate(total=Count('id'))
        ),
        'berry': dict(
            Cake.objects.values_list('berry__name').annotate(total=Count('id'))
        ),
        'decor': dict(
            Cake.objects.values_list('decor__name').annotate(total=Count('id'))
        )
    }
    return statistics

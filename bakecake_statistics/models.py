from django.db import models

from shop.models import Order


class OrderStatistics(Order):

    class Meta:
        proxy = True
        verbose_name_plural = 'статистика по магазину'

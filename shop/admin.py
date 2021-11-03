import csv

from django.contrib import admin
from django.contrib.admin import sites
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.urls import path

from .models import (Berry, Cake, CakeForm, CakeLevel, CancellationOrder,
                     Decor, Order, PromoCode, Topping)
from bakecake_statistics.models import OrderStatistics
from bakecake_statistics.stat_utils import get_statistics


User = get_user_model()


class BakeCakeAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        try:
            reordered_app_list = [
                app_list[2],
                app_list[0],
                app_list[1]
            ]
        except IndexError:
            return app_list
        return reordered_app_list

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('stat_in_csv/', self.export_as_csv, name='stat_in_csv')
        ]
        return my_urls + urls

    def export_as_csv(self, request):
        statistics = get_statistics()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=BC_stat.csv'
        writer = csv.writer(response)
        for stat_obj in statistics:
            if None in statistics[stat_obj]:
                del statistics[stat_obj][None]
            elif 'Без топпинга' in statistics[stat_obj]:
                del statistics[stat_obj]['Без топпинга']
            else:
                writer.writerows(statistics[stat_obj].items())
                writer.writerow([' '])
        return response


bake_cake_site = BakeCakeAdminSite()
admin.site = bake_cake_site
sites.site = bake_cake_site
admin.site.index_title = 'Управление магазином BakeCake'


@admin.register(OrderStatistics)
class BakeCakeStatAdmin(admin.ModelAdmin):
    change_list_template = 'admin/bakecake_statistics.html'

    def get_model_perms(self, request):
        return {'view': True}

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        response.context_data['summary'] = get_statistics()
        return response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'cake', 'destination', 'delivery_time', 'total_price']
    list_display_links = ['cake']


admin.site.register([CakeLevel,
                     CakeForm,
                     Topping,
                     Berry,
                     Decor,
                     Cake,
                     CancellationOrder,
                     PromoCode,
                     User])

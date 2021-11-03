from django.contrib.auth.decorators import login_required

from django import urls
from django.http import JsonResponse
from django.shortcuts import redirect, render

from shop.models import PromoCode
from .forms import CakeConstructorForm, OrderDetailsForm


def show_main_page(request):
    return render(request, 'super_main.html')


@login_required
def make_cake_page(request):
    form = CakeConstructorForm()
    context = {'form': form}
    return render(
        request,
        'cake_constructor.html',
        context=context
    )


@login_required
def order_details(request):
    if request.method == 'GET':
        return redirect(urls.reverse('make_cake_page'))
    cake_form = CakeConstructorForm(data=request.POST)
    cake_form.is_valid()
    prices = []
    for obj in cake_form.cleaned_data.values():
        try:
            prices.extend(obj.values_list('price', flat=True))
        except AttributeError:
            # если объект не кверисет, а объект конкретной записи
            try:
                prices.append(obj.price)
            # если у объекта конкретной записи нет атрибута "цена"
            except AttributeError:
                pass
    total_price = sum(prices)
    order_form = OrderDetailsForm(
        initial={'price': total_price, 'destination': request.user.address}
    )
    return render(
        request,
        'order_details.html',
        {'order_form': order_form, 'cake_form': cake_form, 'price': total_price}
    )


@login_required
def make_order(request):
    if request.method == 'GET':
        return redirect(urls.reverse('make_cake_page'))
    order_form = OrderDetailsForm(data=request.POST)
    order_form.is_valid()
    # создаём запись о заказанном торте
    cake_form = CakeConstructorForm(data=request.POST)
    cake_form.is_valid()
    new_cake = cake_form.save(commit=False)
    new_cake.save()
    cake_form.save_m2m()
    # берем итоговую цену заказа (генерируется на фронте,см.`static/promo.js`)
    total_price = request.POST.get('cake_price')
    # берем при наличии промокод (проверяется на фронте,см.`static/promo.js`)
    if request.POST.get('promo_code'):
        promo_code = PromoCode.objects.get(code=request.POST.get('promo_code'))
    else:
        promo_code = None
    # создаём запись о заказе
    new_order = order_form.save(commit=False)
    new_order.client = request.user
    new_order.promo_code = promo_code
    new_order.total_price = total_price
    new_order.cake = new_cake
    new_order.save()
    return redirect(urls.reverse('account'))


def get_and_check_promo_code(request):
    actualPromoCode = PromoCode.objects.last()
    if not actualPromoCode:
        return JsonResponse(
            {'actualCode': None, 'thisClientUsed': False}
        )
    code_is_used = request.user.orders.filter(
        promo_code__code=actualPromoCode
    ).exists()
    return JsonResponse(
        {'actualCode': actualPromoCode.code, 'thisClientUsed': code_is_used}
    )

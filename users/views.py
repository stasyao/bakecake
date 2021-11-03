from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from shop.models import Order

from .forms import CancellationOrderForm, CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@login_required
def show_orders(request):
    return render(request=request, template_name='user.html', context={'user': request.user})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = CancellationOrderForm(request.POST)
        if form.is_valid():
            canceled_order = form.save(commit=False)
            canceled_order.order = order
            canceled_order.save()
            order.status = 5
            order.save()
            return redirect(reverse_lazy('account'))
    form = CancellationOrderForm()
    return render(request, 'cancellation.html', {'form': form})

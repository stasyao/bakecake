from django.urls import path
from .views import SignUpView, show_orders, cancel_order


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('account/', show_orders, name='account'),
    path('cancel/<int:order_id>', cancel_order, name='cancel'),
]

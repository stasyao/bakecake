import datetime

from django import forms
from django.forms.widgets import (
    CheckboxSelectMultiple, RadioSelect, TextInput, Textarea
)

from shop.models import Cake, Order, Topping, CakeLevel, CakeForm


class CakeConstructorForm(forms.ModelForm):

    def __init__(self, **kwargs):
        kwargs['initial'] = {
            'level': CakeLevel.objects.first(),
            'form': CakeForm.objects.first(),
            'topping': Topping.objects.first()
        }
        super().__init__(**kwargs)
        for field in self.fields:
            self.fields[field].required = False

    class Meta:
        model = Cake
        fields = '__all__'
        help_texts = {
            'caption_on_cake': ('Можно сделать надпись, например '
                                '"С днем рождения!". '
                                'Но, пожалуйста, уложитесь в 45 символов.')
        }
        widgets = {
            'level': RadioSelect(),
            'form': RadioSelect(),
            'topping': RadioSelect(),
            'berry': CheckboxSelectMultiple(),
            'decor': CheckboxSelectMultiple(),
            'caption_on_cake': TextInput(
                attrs={'class': "form-control border border-secondary"}
            )
        }


def initial_datetime():
    initial = datetime.datetime.today() + datetime.timedelta(hours=5)
    initial = initial.strftime("%Y-%m-%dT%H:%M")
    return initial


class OrderDetailsForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['destination', 'comment', 'delivery_time']
        labels = {
            'destination': 'Куда привезти',
            'delivery_time': 'Когда'
        }
        help_texts = {
            'delivery_time': 'Минимальное время доставки 5 часов.'
        }
        widgets = {
            'destination': TextInput(attrs={'class': 'form-control'}),
            'comment': Textarea(attrs={
                'rows': 3,
                'class': ('form-control-sm col-12 mt-0 pt-0 mb-3 border'
                          ' border-2')}
            ),
            'delivery_time': TextInput(
                attrs={
                    'class': 'form-control-sm border border-2',
                    'type': 'datetime-local',
                    'min': initial_datetime()
                }
            )
        }

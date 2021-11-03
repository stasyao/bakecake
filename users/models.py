from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def validate_agreement(value):
    if not value:
        raise ValidationError(
            'Для регистрации необходимо согласиться на обработку персональных данных.'
        )


class CustomUser(AbstractUser):

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50
    )
    phonenumber = PhoneNumberField(
        verbose_name='Телефон',
    )
    social_network = models.CharField(
        'Ссылка на соцсеть',
        max_length=100,
        blank=True,
    )
    address = models.CharField(
        'Адрес',
        max_length=200,
    )

    agreement = models.BooleanField(
        'Согласие на обработку персональных даных',
        validators=[validate_agreement],
        default=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} {self.first_name} {self.last_name}'


class UsersCount(CustomUser):
    class Meta:
        proxy = True
        verbose_name = 'Статистика по пользователям'
        verbose_name_plural = 'Статистика по пользователям'

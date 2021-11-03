# Generated by Django 3.2.8 on 2021-10-29 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='промокод')),
            ],
        ),
        migrations.AlterModelOptions(
            name='berry',
            options={'ordering': ('price',)},
        ),
        migrations.AlterModelOptions(
            name='cakeform',
            options={'ordering': ('price',)},
        ),
        migrations.AlterModelOptions(
            name='cakelevel',
            options={'ordering': ('price',)},
        ),
        migrations.AlterModelOptions(
            name='decor',
            options={'ordering': ('price',)},
        ),
        migrations.AlterModelOptions(
            name='topping',
            options={'ordering': ('price',)},
        ),
        migrations.RemoveField(
            model_name='cakelevel',
            name='level',
        ),
        migrations.AddField(
            model_name='cake',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.cakeform', verbose_name='форма торта'),
        ),
        migrations.AddField(
            model_name='cakelevel',
            name='level_num',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='число уровней торта'),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.PositiveSmallIntegerField(db_index=True, default=1, verbose_name='цена заказа'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='berry',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='berry',
            name='price',
            field=models.PositiveSmallIntegerField(verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='cake',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.cakelevel', verbose_name='число уровней'),
        ),
        migrations.RemoveField(
            model_name='cake',
            name='topping',
        ),
        migrations.AddField(
            model_name='cake',
            name='topping',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.topping', verbose_name='топпинги'),
        ),
        migrations.AlterField(
            model_name='cakeform',
            name='price',
            field=models.PositiveSmallIntegerField(verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='cakeform',
            name='type',
            field=models.CharField(max_length=100, unique=True, verbose_name='тип'),
        ),
        migrations.AlterField(
            model_name='cakelevel',
            name='price',
            field=models.PositiveSmallIntegerField(verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='decor',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='decor',
            name='price',
            field=models.PositiveSmallIntegerField(verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cake',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.cake', verbose_name='торт'),
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='клиент'),
        ),
        migrations.AlterField(
            model_name='topping',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='topping',
            name='price',
            field=models.PositiveSmallIntegerField(verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='shop.promocode', verbose_name='промокод'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-29 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0026_remove_orderproduct_color_remove_sizes_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaidGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Когда купили товар товар')),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loft.shippingaddress', verbose_name='Адресс получателя')),
                ('customer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loft.customer', verbose_name='Клиент')),
                ('products', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loft.orderproduct', verbose_name='Заказанный товар')),
            ],
            options={
                'verbose_name': 'Оплаченный товар',
                'verbose_name_plural': 'Оплаченные товары',
            },
        ),
    ]

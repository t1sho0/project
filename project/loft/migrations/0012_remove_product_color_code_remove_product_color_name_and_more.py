# Generated by Django 5.0.2 on 2024-02-10 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0011_customer_order_orderproduct_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color_code',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color_name',
        ),
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(max_length=150, verbose_name='Название цвета')),
                ('color_code', models.CharField(max_length=400, verbose_name='Код цвета')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loft.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Цвет товара',
                'verbose_name_plural': 'Цвета товаров',
            },
        ),
    ]

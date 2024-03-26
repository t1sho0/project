# Generated by Django 5.0.1 on 2024-02-04 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0009_message_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dop_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dop_products', to='loft.category', verbose_name='Доп категория'),
        ),
    ]

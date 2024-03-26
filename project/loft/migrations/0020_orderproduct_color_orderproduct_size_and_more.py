# Generated by Django 5.0.1 on 2024-02-18 06:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0019_alter_profile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loft.colors', verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='size',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='loft.sizes', verbose_name='Размеры'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name='Количество'),
        ),
    ]
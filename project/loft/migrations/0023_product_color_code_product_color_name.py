# Generated by Django 5.0.1 on 2024-02-21 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0022_alter_orderproduct_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color_code',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Код цвета'),
        ),
        migrations.AddField(
            model_name='product',
            name='color_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Название цвета'),
        ),
    ]

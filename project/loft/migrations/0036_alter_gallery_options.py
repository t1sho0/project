# Generated by Django 5.0.1 on 2024-03-17 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0035_rename_created_at_orderproduct_added_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallery',
            options={'verbose_name': 'Картинка Товара', 'verbose_name_plural': 'Картинки Товаров'},
        ),
    ]
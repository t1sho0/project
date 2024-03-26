# Generated by Django 5.0.1 on 2024-02-22 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0025_rename_depth_product_size_depth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='sizes',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
        migrations.AlterModelOptions(
            name='gallery',
            options={'verbose_name': 'Размер Товара', 'verbose_name_plural': 'Размеры Товаров'},
        ),
        migrations.DeleteModel(
            name='Colors',
        ),
        migrations.DeleteModel(
            name='Sizes',
        ),
    ]

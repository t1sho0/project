# Generated by Django 5.0.1 on 2024-02-17 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0015_remove_product_depth_remove_product_height_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='Город'),
        ),
    ]

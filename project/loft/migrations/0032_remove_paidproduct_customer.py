# Generated by Django 5.0.1 on 2024-03-13 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0031_paidproduct_customer_paidproduct_is_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paidproduct',
            name='customer',
        ),
    ]
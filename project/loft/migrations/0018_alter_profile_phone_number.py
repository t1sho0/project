# Generated by Django 5.0.1 on 2024-02-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0017_delete_productdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='Номер телефона'),
        ),
    ]
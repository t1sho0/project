# Generated by Django 5.0.1 on 2024-01-29 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loft', '0006_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='model_product',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Модель'),
        ),
    ]
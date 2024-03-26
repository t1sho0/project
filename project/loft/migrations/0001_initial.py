# Generated by Django 5.0.1 on 2024-01-24 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название категории')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Картинка')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='loft.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название товара')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('credit', models.CharField(blank=True, max_length=250, null=True, verbose_name='Рассрочка')),
                ('discount', models.CharField(blank=True, max_length=250, null=True, verbose_name='Скидка')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('memory', models.CharField(max_length=250, verbose_name='Память')),
                ('color_name', models.CharField(max_length=150, verbose_name='Название цвета')),
                ('color_code', models.CharField(max_length=150, verbose_name='Код цвета')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='loft.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/', verbose_name='Картинка товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='loft.product')),
            ],
            options={
                'verbose_name': 'Картинка Товара',
                'verbose_name_plural': 'Картинки Товаров',
            },
        ),
        migrations.CreateModel(
            name='ProductDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.CharField(max_length=150, verbose_name='Название параметра')),
                ('parameter_info', models.CharField(max_length=400, verbose_name='Описание параметра')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loft.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Описание Товара',
                'verbose_name_plural': 'Описание Товаров',
            },
        ),
    ]

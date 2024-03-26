from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Картинка')
    slug = models.SlugField(unique=True, null=True)

    def get_absolute_url(self):
        return reverse('category_page', kwargs={'slug': self.slug})

    # Метод для получения картинки категории
    def get_image_category(self):
        if self.image:
            return self.image.url
        else:
            return ''

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название товара')
    price = models.FloatField(verbose_name='Цена')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name='описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    short = models.TextField(max_length=150, blank=True, null=True, verbose_name='Краткое описание')
    slug = models.SlugField(unique=True, null=True)
    model_product = models.CharField(max_length=300, verbose_name='Модель', null=True, blank=True)
    dop_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dop_products', blank=True,
                                     null=True, verbose_name='Доп категория')
    discount = models.CharField(max_length=150, blank=True, null=True, verbose_name='Скидка')
    color_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Название цвета')
    color_code = models.CharField(max_length=150, blank=True, null=True, verbose_name='Код цвета')
    size_width = models.CharField(max_length=150, verbose_name='Ширина', blank=True, null=True)
    size_depth = models.CharField(max_length=400, verbose_name='Глибина', blank=True, null=True)
    size_height = models.CharField(max_length=400, verbose_name='Высота', blank=True, null=True)
    size_long = models.CharField(max_length=400, verbose_name='Длина', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_price_by_discount(self):
        if Product.discount:
            discount = int(self.price) / 100 * int(self.discount)
            result = int(self.price) - discount
            return result

    def get_image_product(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return '-'
        else:
            return '-'

    def get_all_images_product(self):
        if self.images:
            try:
                return [image.image.url for image in self.images.all()[1:]]
            except:
                return '-'
        else:
            return '-'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Картинка товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Картинка Товара'
        verbose_name_plural = 'Картинки Товаров'


class Message(models.Model):
    name = models.CharField(max_length=300, verbose_name='Имя')
    email = models.CharField(max_length=300, verbose_name='почта')
    text = models.CharField(max_length=300, verbose_name='Саобщение')
    file = models.FileField(upload_to='messages/', blank=True, null=True, verbose_name='Файл')

    class Meta:
        verbose_name = 'Саобщение'
        verbose_name_plural = 'Саобшении'


class FavoriteProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Избранный товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'Товар:{self.product}, пользователя: {self.user.username}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные товары'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255, default='', verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=255, default='', verbose_name='Фамилия покупателя')
    email = models.EmailField(verbose_name='Почта покупателя', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнен ли заказ')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return f'Заказа №: {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity

    def get_price_for_paid(self):
        order_products = self.orderproduct_set.all()
        for product in order_products:
            return product.price
            # if product.product.discount:
            #     discount = int(product.product.price) / 100 * int(product.product.discount)
            #     result = int(self.price) - discount
            #     return result
            # else:
            #     return product.product.price


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ №')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    @property
    def get_total_price(self):
        if self.product.discount:
            total_price = self.product.price * self.quantity
            discount = total_price / 100 * int(self.product.discount)
            result = total_price - discount
            return result
        else:
            total_price = self.product.price * self.quantity
            return total_price


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone_number = models.CharField(max_length=350, blank=True, null=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=350, blank=True, null=True, verbose_name='Город')
    street = models.CharField(max_length=350, blank=True, null=True, verbose_name='Улица')
    home = models.CharField(max_length=200, blank=True, null=True, verbose_name='Дом/Корпус')
    house = models.CharField(max_length=200, blank=True, null=True, verbose_name='Квартира')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=300, verbose_name='Адрес улица/дом')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город доставки')
    region = models.CharField(max_length=255, verbose_name='Регион/Область')
    phone = models.CharField(max_length=255, verbose_name='Номер телефона')
    comment = models.CharField(max_length=500, verbose_name='Комментарий к заказу', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата доставки')

    def __str__(self):
        return f'Доставка заказа №:{self.order} по Адресу:{self.address}'

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставок'


class City(models.Model):
    city_name = models.CharField(max_length=100, verbose_name='Название города')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Paid(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Состояние заказа')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')
    # price = models.FloatField(blank=True, null=True, verbose_name='Сумма товаров')
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')

    def __str__(self):
        return f'Заказа №: {self.pk}'

    @property
    def get_cart_total_price(self):
        order_products = self.paidproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.paidproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity

    class Meta:
        verbose_name = 'Оплаченный заказ'
        verbose_name_plural = 'Оплаченные заказы'


class PaidProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Товар')
    paid = models.ForeignKey(Paid, on_delete=models.SET_NULL, null=True, verbose_name='Заказ №')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    price = models.FloatField(blank=True, null=True, verbose_name='Цена продукта')
    is_completed = models.BooleanField(default=False, verbose_name='Состояние заказа')

    def __str__(self):
        return self.product.title

    @property
    def get_total_price(self):
        if self.product.discount:
            total_price = self.product.price * self.quantity
            discount = total_price / 100 * int(self.product.discount)
            result = total_price - discount
            return result
        else:
            total_price = self.product.price * self.quantity
            return total_price

    class Meta:
        verbose_name = 'Оплаченный товар'
        verbose_name_plural = 'Оплаченные товары'

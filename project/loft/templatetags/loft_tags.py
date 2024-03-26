from django import template
from loft.models import Product, Category, FavoriteProducts, PaidProduct

register = template.Library()


@register.simple_tag()
def get_products_detail():
    products = Product.objects.all()[::-1][:4]
    return products


@register.simple_tag()
def get_products(category):
    products = Product.objects.filter(category=category)  # | Product.objects.filter(dop_category=category)
    return products


@register.simple_tag()
def get_categories_header():
    return Category.objects.all()[:7]


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_colors(model_product):
    products = Product.objects.filter(model_product=model_product)
    list_colors = [i.color_code for i in products]
    return list_colors


@register.simple_tag()
def get_sizes(model_product):
    products = Product.objects.filter(model_product=model_product)
    sizes = [{
        'width': i.size_width,
        'depth': i.size_depth,
        'height': i.size_height,
        'long': i.size_long
    } for i in products]

    return sizes


@register.simple_tag()
def get_normal_price(price):
    return f'{int(price):_}'.replace('_', ' ')


@register.simple_tag()
def get_favorite_products(user):
    fav_products = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in fav_products]
    return products


@register.simple_tag()
def get_paid_products(user):
    products = PaidProduct.objects.filter(user=user)
    products = [i.product for i in products][::-1][:4]
    return products


@register.simple_tag()
def get_total_price_for_product(price, quantity):
    return int(price) * int(quantity)

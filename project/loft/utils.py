from .models import Product, OrderProduct, Order, Customer, PaidProduct, Paid
from django.contrib import messages


class CartForAuthenticatedUser:
    def __init__(self, request, pk=None, action=None, num=None):
        self.user = request.user
        self.request = request

        if pk and action:
            self.add_or_delete(pk, action, num)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user)

        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.orderproduct_set.all()
        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'order': order,
            'products': order_products
        }

    def add_or_delete(self, pk, action, num):
        order = self.get_cart_info()['order']
        product = Product.objects.get(pk=pk)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0:
            order_product.quantity += num
            product.quantity -= num
            messages.success(self.request, f'Товар {product.title} в корзине')
        else:
            order_product.quantity -= num
            product.quantity += num
            messages.warning(self.request, f'Товар {product.title} удалён из корзины')

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def clear(self):
        order = self.get_cart_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            product.delete()

        order.save()


def get_cart_data(request):
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()
    return cart_info


class SavePaidOrder:
    def __init__(self, request, quantity=None, product=None):
        self.user = request.user
        self.request = request

        if quantity and product:
            self.add_or_delete(product, quantity)

    def get_cart_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user)

        paid, created = Paid.objects.get_or_create(customer=customer)
        paid_products = paid.paidproduct_set.all()
        cart_total_quantity = paid.get_cart_total_quantity
        cart_total_price = paid.get_cart_total_price

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'paid': paid,
            'products': paid_products
        }

    def add_or_delete(self, produc, quantity):
        paid = self.get_cart_info()['paid']
        product = Product.objects.get(pk=produc)
        price = product.price

        paid_product, created = PaidProduct.objects.get_or_create(paid=paid, product=product, price=price, quantity=quantity)
        messages.success(self.request, f'Товар {product.title} в корзине')

        paid_product.save()


def get_paid_data(request):
    cart = SavePaidOrder(request)
    # cart_info = cart.get_cart_info()
    info = cart.get_cart_info()
    return info


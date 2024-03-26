from random import randint
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.views.generic import ListView, DetailView
from .forms import LoginForm, RegisterForm, MessageForm, EditProfileForm, ShippingForm, CustomerForm
from django.contrib import messages
from .utils import CartForAuthenticatedUser, get_cart_data, SavePaidOrder, get_paid_data
import stripe
from project import settings


# Вьюшка страницы о сайте
class AboutView(View):
    def get(self, request):
        return render(request, 'loft/about.html')


# Вьюшка страницы контактов
def contact_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за предложение мы свами свяжемся !')
            return redirect('contact')
        else:
            messages.error(request, 'Что-то пошло не так проверьте заполнили-ли вы все поля')
    else:
        form = MessageForm()

    context = {'form': form}
    return render(request, 'loft/contact.html', context)


class ProductList(ListView):
    model = Product
    context_object_name = 'categories'

    extra_context = {
        'title': 'Loft'
    }

    template_name = 'loft/index.html'

    def get_queryset(self):
        categories = Category.objects.all()[:8]
        return categories


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'loft/category_page.html'

    def get_queryset(self):
        color_field = self.request.GET.get('color')
        size_field = self.request.GET.get('size')
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category) | Product.objects.filter(dop_category=category)

        if color_field:
            products = products.filter(color_name=color_field)

        if size_field:
            products = products.filter(size_width=size_field)

        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category)

        colors = list(set([i.color_name for i in products]))
        sizes = list(set([i.size_width for i in products]))

        context['colors'] = colors
        context['sizes'] = sizes
        context['title'] = f'Категория {category.title}'
        context['category'] = category

        return context


def search_result(request):
    word = request.GET.get('q')
    products = Product.objects.filter(title__icontains=word.lower()) | Product.objects.filter(
        title__icontains=word.capitalize())

    context = {
        'products': products
    }

    return render(request, 'loft/category_page.html', context)


def user_login_view(request):
    if request.user.is_authenticated:
        page = request.META.get('HTTP_REFERER', 'index')
        return redirect(page)
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    messages.success(request, 'Вы вошли в Аккаунт')
                    return redirect('index')
                else:
                    messages.error(request, 'Не верная почта или пароль')
                    return redirect('register')
            else:
                messages.error(request, 'Не верная почта или пароль')
                return redirect('register')
        else:
            form = LoginForm()

        context = {
            'form': form,
            'title': 'Вход в Аккаунт'
        }

        return render(request, 'loft/login.html', context)


def user_logout_view(request):
    logout(request)
    messages.warning(request, 'Вы вышли с аккаунта')
    return redirect('index')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = RegisterForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                messages.success(request, 'Регистрация прошла успешно. Авторизуйтесь')
                return redirect('login')
            else:
                for field in form.errors:
                    messages.error(request, form.errors[field].as_text())
                    return redirect('register')

        else:
            form = RegisterForm()

        context = {
            'form': form,
            'title': 'Регистрация пользователя'
        }

        return render(request, 'loft/register.html', context)


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = f'Товар {product.title}'

        return context


def product_by_color(request, model_product, color_code):
    try:
        product = Product.objects.get(model_product=model_product, color_code=color_code)
    except Product.MultipleObjectsReturned:
        product = Product.objects.filter(model_product=model_product, color_code=color_code).first()
    context = {
        'title': f'Товар {product.title}',
        'product': product,
    }

    return render(request, 'loft/product_detail.html', context)


def product_by_size(request, model_product, size_long, size_width, size_depth, size_height):
    try:
        product = Product.objects.get(model_product=model_product, size_long=size_long, size_width=size_width,
                                      size_depth=size_depth, size_height=size_height)
    except Product.MultipleObjectsReturned:
        product = Product.objects.filter(model_product=model_product, size_width=size_width).first()

    context = {
        'title': f'Товар {product.title}',
        'product': product,
    }

    return render(request, 'loft/product_detail.html', context)


def save_favorite_product(request, slug):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(slug=slug)
        favorite_products = FavoriteProducts.objects.filter(user=user)
        if user:
            if product not in [i.product for i in favorite_products]:
                messages.success(request, f'Товар добавлен в избранное')
                FavoriteProducts.objects.create(user=user, product=product)
            else:
                fav_product = FavoriteProducts.objects.get(user=user, product=product)
                messages.error(request, f'Товар удалён из избранного')
                fav_product.delete()

            page = request.META.get('HTTP_REFERER', 'index')
            return redirect(page)

    else:
        messages.warning(request, 'Авторизуйтесь что бы добавить в избранное')
        return redirect('login')


class FavoriteProductView(LoginRequiredMixin, ListView):
    model = FavoriteProducts
    template_name = 'loft/favorite.html'
    context_object_name = 'products'
    login_url = 'login'

    def get_queryset(self):
        user = self.request.user
        favorite_products = FavoriteProducts.objects.filter(user=user)
        products = [i.product for i in favorite_products]
        return products


def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)
    info = get_paid_data(request)

    context = {
        'title': f'Профиль: {profile.user.username}',
        'profile': profile,
        'edit_profile_form': EditProfileForm(instance=request.user.profile if request.user.is_authenticated else None),
        'paid': info['paid'],
        'products': info['products']
    }

    return render(request, 'loft/profile.html', context)


def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('profile', pk=request.user.pk)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field])
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'loft/profile.html', {'edit_profile_form': form})


def basket_view(request, pk, action, num):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, pk, action, num)
        page = request.META.get('HTTP_REFERER', 'index')
        return redirect(page)

    else:
        return redirect('login')


def my_basket_view(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)
        context = {
            'title': 'Моя корзина',
            'order': cart_info['order'],
            'products': cart_info['products']
        }
        return render(request, 'loft/basket.html', context)

    else:
        return redirect('login')


def clear_cart(request):
    user_cart = CartForAuthenticatedUser(request)
    order = user_cart.get_cart_info()['order']
    order_products = order.orderproduct_set.all()
    for order_product in order_products:
        quantity = order_product.quantity
        product = order_product.product
        order_product.delete()
        product.quantity += quantity
        product.save()
    messages.warning(request, 'Корзина очищена')
    return redirect('basket')


def clear_cart_product(request, product_id):
    user_cart = CartForAuthenticatedUser(request)
    order = user_cart.get_cart_info()['order']

    try:
        order_product = order.orderproduct_set.get(product_id=product_id)
        quantity = order_product.quantity
        product = order_product.product
        product.quantity += quantity

        # Удаляем продукт из заказа
        order_product.delete()
        product.save()

        messages.warning(request, f'Продукт {product.title} удален из корзины')
    except order.orderproduct_set.model.DoesNotExist:
        messages.error(request, 'Продукт не найден в корзине')

    return redirect('my_basket')


def checkout_view(request):
    if request.user.is_authenticated:
        cart_info = get_cart_data(request)

        context = {
            'title': 'Оформление заказа',
            'order': cart_info['order'],
            'items': cart_info['products'],

            'customer_form': CustomerForm(),
            'shipping_form': ShippingForm()
        }
        return render(request, 'loft/checkout.html', context)

    else:
        return redirect('login')


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data['first_name']
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.email = customer_form.cleaned_data['email']
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            address = shipping_form.save(commit=False)
            address.customer = Customer.objects.get(user=request.user)
            address.order = user_cart.get_cart_info()['order']
            address.save()
        else:
            for field in shipping_form.errors:
                messages.error(request, shipping_form.errors[field].as_text())

        total_price = cart_info['cart_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Товары LoftМебель'
                    },
                    'unit_amount': int(total_price)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )
        return redirect(session.url, 303)


def success_payment(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
        products = user_cart.get_cart_info()['products']
        quantity = user_cart.get_cart_info()['cart_total_quantity']
        for order_product in products:
            global pk
            pk = order_product.product.pk

        # product = Product.objects.get(pk=pk)

        save = SavePaidOrder(request, quantity, pk)

        user_cart.clear()
        messages.success(request, 'Ваша оплата прошла успешно. Мы отправим вам подтверждение заказа.')
        return render(request, 'loft/success.html')

    else:
        return redirect('index')

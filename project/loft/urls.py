# from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('category_page/<slug:slug>/', CategoryView.as_view(), name='category_page'),
    path('search/', search_result, name='search'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', contact_view, name='contact'),
    path('product_detail/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('product_color/<str:model_product>/<str:color_code>/', product_by_color, name='product_color'),
    path('product_size/<str:model_product>/<str:size_long>/<str:size_width>/<str:size_depth>/<str:size_height>/', product_by_size, name='product_size'),
    path('save_favorite/<slug:slug>/', save_favorite_product, name='save_favorite'),
    path('favorite/', FavoriteProductView.as_view(), name='favorite'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
    path('basket_view/<int:pk>/<str:action>/<int:num>/', basket_view, name='basket'),
    path('my_basket/', my_basket_view, name='my_basket'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('clear_cart_product/<int:product_id>/', clear_cart_product, name='clear_cart_product'),
    path('checkout/', checkout_view, name='checkout'),
    path('success/', success_payment, name='success'),
    path('payment/', create_checkout_session, name='payment')
]

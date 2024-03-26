from django.contrib import admin
from .models import *
from .forms import CategoryForm, MessageForm
from django.utils.safestring import mark_safe


# Register your models here.

class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'get_image')
    form = CategoryForm
    prepopulated_fields = {'slug': ['title']}

    # МЕТОД ДЛЯ ПОЛУЧЕНИЯ КАРТИНКИ КАТЕГОРИИ
    def get_image(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="75" >')
            except:
                return '-'
        else:
            return '-'

    get_image.short_description = 'Картинка'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'get_image')
    list_display_links = ('pk', 'title')
    prepopulated_fields = {'slug': ['title']}
    inlines = [GalleryInline]
    list_editable = ['quantity']

    def get_image(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75" >')
            except:
                return '-'
        else:
            return '-'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'email', 'file', 'text')
    form = MessageForm

@admin.register(PaidProduct)
class PaidProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'added_at')
    form = MessageForm




admin.site.register(Gallery)
admin.site.register(FavoriteProducts)

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Customer)
admin.site.register(Profile)
admin.site.register(ShippingAddress)
admin.site.register(City)
admin.site.register(Paid)
# admin.site.register(PaidProduct)

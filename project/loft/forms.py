from django import forms
from .models import Category, Message, Profile, Customer, ShippingAddress, City
from django_svg_image_form_field import SvgAndImageFormField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        field_classes = {
            'image': SvgAndImageFormField,
        }


# Форма входа в Аккаунт
class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваша почта'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Пароль'
    }))


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваше имя'
    }))

    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваша фамилия'
    }))

    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваша почта'
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Номер телефона'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Подтведите пароль'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'phone_number', 'password1', 'password2')


class MessageForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваше имя'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваша почта'
    }))

    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-message',
        'placeholder': 'Сообщение'
    }))

    file = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control ',
        'placeholder': 'Файл'
    }))

    class Meta:
        model = Message
        fields = ('name', 'email', 'text', 'file')


class EditProfileForm(forms.ModelForm):
    username = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваша почта'
    }))

    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваше имя'
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Ваша фамилия'
    }))

    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Номер телефона'
    }))

    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Город'
    }))

    street = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Улица'
    }))

    home = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Дом/Корпус'
    }))

    house = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control contact__section-input',
        'placeholder': 'Квартира'
    }))

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'city', 'street', 'home', 'house']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control contact__section-input',
                'placeholder': 'Имя получателя...'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control contact__section-input',
                'placeholder': 'Фамилия полкчателя...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control contact__section-input',
                'placeholder': 'Почта полкчателя...'
            })

        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('address', 'city', 'region', 'phone', 'comment')
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control contact__section-input',
                'placeholder': 'Адрес...'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select contact__section-input',
                'placeholder': 'Город...'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control contact__section-input',
                'placeholder': 'Регион...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control contact__section-input',
                'placeholder': 'Номер телефона...'
            }),
            'comment': forms.TextInput(attrs={
                'class': 'form-control contact__section-message',
                'placeholder': 'Комментарий к заказу...'
            })

        }

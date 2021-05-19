from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


User = get_user_model()
#
#
# class CreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ("name", "surname", "email")

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', help_text='Some message:)', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Passw', widget=forms.PasswordInput(attrs={'class': 'form-control'}))




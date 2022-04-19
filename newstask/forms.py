from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator

from newstask.models import News


class UserRegisterForm(UserCreationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                validators=[MinLengthValidator(8),
                                            RegexValidator(regex=r'(?=.*[A-Za-z])(?=.*[0-9])[A-Za-z0-9]{8,}',
                                                           message='Password must contain at least 1 letter and at least 1 number')])
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                validators=[MinLengthValidator(8),
                                            RegexValidator(regex=r'(?=.*[A-Za-z])(?=.*[0-9])[A-Za-z0-9]{8,}')])
    author = forms.BooleanField(label='Became author', widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'access_category']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
                   'access_category': forms.Select(attrs={'class': 'form-control'})}

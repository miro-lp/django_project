from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from YouTravel.accounts.models import TravelProfile
from YouTravel.core.forms import BootstrapFormMixin

UserModel = get_user_model()


class LoginForm(BootstrapFormMixin, forms.Form):
    user = None
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput()

    )

    def clean_password(self):
        self.user = authenticate(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        if not self.user:
            raise ValidationError('Email/Password is incorrect')

    def save(self):
        return self.user


class RegisterForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TravelProfile
        exclude = ('user', 'friends',)
        fields = '__all__'

    def clean(self):
        if len(self.cleaned_data['first_name']) <= 3:
            raise ValidationError('Title must have more than 3 symbols')
        if not self.cleaned_data['first_name'][0].isupper():
            raise ValidationError('Title must start with capitalized letter')


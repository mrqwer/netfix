from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    birth = forms.DateField(
        label="Choose a birth",
        widget = DateInput(attrs={'type': 'date'}),
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_customer = True
        if commit:
            user.save()

            if self.cleaned_data.get("birth"):
                birth = self.cleaned_data["birth"]
                customer = Customer(user=user, birth=birth)
                customer.save()

        return user

    class Meta:
        model = User
        fields = ("username", "email")


class CompanySignUpForm(UserCreationForm):
    field_of_work_choices = [
        ('AC', 'Air Conditioner'),
        ('AIO', 'All in One'),
        ('CAR', 'Carpentry'),
        ('ELE', 'Electricity'),
        ('GAR', 'Gardening'),
        ('HM', 'Home Machines'),
        ('HK', 'Housekeeping'),
        ('ID', 'Interior Design'),
        ('LOC', 'Locks'),
        ('PAI', 'Painting'),
        ('PLU', 'Plumbing'),
        ('WH', 'Water Heaters'),
    ]
    field_of_work = forms.ChoiceField(
        choices=field_of_work_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_company = True
        if commit:
            user.save()

            if self.cleaned_data.get("field_of_work"):
                company_field = self.cleaned_data["field_of_work"]
                company = Company(user=user, field=company_field)
                company.save()

        return user
    class Meta:
        model = User
        fields = ("username", "email",)


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs['autocomplete'] = 'off'

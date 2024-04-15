from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserInfo


# form to show up on the register page to get information to enter a new user and userinfo
class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='\n')
    user_name = forms.CharField(max_length=50, help_text='\n')
    first_name = forms.CharField(max_length=20, help_text='\n')
    last_name = forms.CharField(max_length=20, help_text='\n')
    # choice filed to define whether the user is a driver or a non driver
    is_driver = forms.ChoiceField(label='Are you a user or a driver?', choices=(('False','User'),('True','Driver')), help_text='\n')
    # 2 password fields to ensure that the user has entered the password correctly
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50, label='Password', help_text='\n')
    password2 = forms.CharField(widget=forms.PasswordInput(), max_length=50, label='Reenter Password')

    # checks if the email already exists in the database
    def clean_email(self):
        email = self.cleaned_data['email']
        # if the email exists, raise a validation error
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        # return the email if its valid
        return email

    # checks if the entered username already exists in the database
    def clean_user_name(self):
        username = self.cleaned_data['user_name']
        # if the username exists, raise a validation error
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        # return the username if its valid
        return username

    # checks if the passwords match and if they are complex enough
    # partially retrieved from https://stackoverflow.com/questions/7948750/custom-form-validation
    def clean(self):
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password2']:
            self._errors["password"] = ["Password does not match"]
            del form_data['password']
        return form_data

    # meta information to define the form fields
    class Meta:
        model = User
        fields = ('email', 'user_name', 'first_name', 'last_name', 'is_driver', 'password', 'password2', )


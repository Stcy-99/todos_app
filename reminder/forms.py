from django import forms
from django.contrib.auth.models import User
from reminder.models import Todos
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    password2=forms.CharField()
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class SignInForm(forms.Form):
    username=forms.CharField( widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

class TodoForm(forms.ModelForm):
    class Meta:
        model=Todos
        fields=["name"]

from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2',)
        
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('phone','gender','company_name','image','user','type','status')
        widgets = {'user': forms.HiddenInput(),'type': forms.HiddenInput(),'status': forms.HiddenInput()}
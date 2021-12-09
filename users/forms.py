from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm



class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name' , 'email' , 'username' , 'password1', 'password2']
        labels = {
            'first_name' : 'Name',
        }
        

    def __init__(self, *args, **kwargs) -> None:
        super(SignupForm,self).__init__(*args, **kwargs)
        

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            
            if name == 'username':
                field.help_text = 'Letters, digits and @/./+/-/_ only.' 
            elif name  == 'password1':
                field.help_text = '<li>Your password must contain at least 8 characters</li><li>Must not be entirely numeric</li>' 
            else:
                field.help_text = None

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        

    def __init__(self , *args , **kwargs):
        super().__init__(*args , **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
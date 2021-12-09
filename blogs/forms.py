from django import forms
from django.db.models.base import Model
from .models import Blog, Image, Review
from django.forms import ModelForm


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ['writer','created' , 'updated' , 'id' ,'vote_total','vote_ratio']

        widgets = {
            'tags': forms.CheckboxSelectMultiple 
        }

    def __init__(self , *args, **kwargs):
        super(BlogForm , self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})

    def data(self):
        print(self.data)


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['image_x']

        labels = {
            'image_x': 'Do you wish to add any extra images to the blog?'
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value' , 'body']
    
    def __init__(self , *args, **kwargs):
        super(ReviewForm , self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})
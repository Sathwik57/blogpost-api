from django.contrib import admin
from .models import Image, Review, Tag,Blog

# Register your models here.

admin.site.register(Blog)
admin.site.register(Tag)
admin.site.register(Image)

admin.site.register(Review)
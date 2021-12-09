from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home , name= 'home'),
    path('add-blog/', views.add_blog , name= 'add-blog'),
    path('view-blog/<str:pk>/', views.view_blog , name= 'view-blog'),
    path('blog/<str:pk>/addimg/', views.add_images , name= 'blog-images'),
    path('blogs/', views.all_blogs , name= 'blogs-all'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
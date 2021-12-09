from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>/', views.account, name= 'account'),
    path('login/', views.login_user , name= 'login_user'),
    path('register/', views.register_user , name= 'register_user'),
    path('logout/', views.logout_user, name= 'logout'),
    path('update-profile/', views.update_profile, name= 'update-profile'),
    path('timeline/', views.timeline, name= 'timeline'),
    path('follow/<str:pk>/', views.follow, name= 'follow'),
    path('unfollow/<str:pk>/', views.unfollow, name= 'unfollow'),
    path('writers/', views.writers, name= 'writers'),
]
from django.urls import path
from ..views import user_views

urlpatterns = [
    path('', user_views.WriterList.as_view(),name ='writer-list' ),
    path('create/', user_views.CreateWriter.as_view(),name ='create-writer' ),
    path('profile/<str:pk>/', user_views.ViewWriter.as_view(),name ='writer' ),
    path('profile/<str:pk>/update/', user_views.UpdateProfile.as_view(),name ='update-profile' ),
    path('profile/<str:pk>/delete/', user_views.DeleteProfile.as_view(),name ='delete-profile' ),
    path('profile/<str:pk>/followers/', user_views.FollowersList.as_view(),name ='followers' ),
    path('profile/<str:pk>/following/', user_views.FollowingList.as_view(),name ='following' ),
    path('profile/<str:pk>/follow/', user_views.FollowUser.as_view(),name ='follow' ),
    path('profile/<str:pk>/unfollow/', user_views.UnFollow.as_view(),name ='unfollow' ),
    path('profile/<str:pk>/timeline/', user_views.Timeline.as_view(),name ='timeline' ),
]
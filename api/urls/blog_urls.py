from django.urls import path
from ..views import blog_views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', blog_views.get_routes,name='api'),

    path('blogs/',blog_views.GetBlogs.as_view() , name ='blogs'),
    path('blog/create/',blog_views.CreateBlog.as_view() , name ='create-blog'),
    path('blog/<str:pk>/view/',blog_views.ViewBlog.as_view() , name ='view-blog'),
    path('blog/<str:pk>/update/',blog_views.UpdateDetailBlog.as_view() , name ='update-blog'),
    path('blog/<str:pk>/delete/',blog_views.DeleteBlog.as_view() , name ='delete-blog'),

    path('blog/<str:pk>/vote/',blog_views.AddReview.as_view(),name='vote-blog'),
    path('blog/<str:pk>/reviews/',blog_views.ReviewList.as_view(),name='blog-reviews'),

    path('tags/', blog_views.TagList.as_view(),name = 'tag-list'), 
    path('tag/create', blog_views.CreateTag.as_view(),name = 'tag-create'),
    path('tag/<str:pk>/', blog_views.ViewTag.as_view(),name = 'tag-view'),
    path('tag/<str:pk>/delete', blog_views.DeleteTag.as_view(),name = 'tag-delete'),

    path('token/',obtain_auth_token , name ='token'),
]
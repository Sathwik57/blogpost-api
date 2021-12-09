from http.client import HTTP_PORT
from django.http import  Http404
from django.http.response import HttpResponse
from rest_framework.permissions import   IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import  serializers, status  
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView, DestroyAPIView, 
    ListAPIView,RetrieveAPIView, 
    RetrieveUpdateAPIView, 
)

#Local imports
from api.perm import IsUser, ValidUser
from api.serializers import BlogSerializer, FollowSerializer, ProfileSerializer, UserSerializer
from blogs.models import Blog
from users.models import Follow, Profile

class CreateWriter(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        try:
            return super().perform_create(serializer)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class WriterList(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ViewWriter(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            profile =self.get_object()
            resp =  super().retrieve(request, *args, **kwargs)
            blogs = list(profile.blog_set.all().order_by('-vote_total')[:3])
            serializer = BlogSerializer(blogs ,many = True ,context = {'page': 'profile'})    
            resp.data['no_of_blogs'] = profile.blog_count().count()
            resp.data['blogs'] = serializer.data
            return Response(resp.data)
        except:
            return Response({'Invalid':'User not found'},status=status.HTTP_404_NOT_FOUND)

class UpdateProfile(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,IsUser,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    #TODO: Need to find a way to raise 404 fro dispatch method 
    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         profile =self.get_object()
    #     except:
    #         raise Http404
    #     return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        try:
            profile =self.get_object()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        try:
            profile =self.get_object()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        try:
            profile =self.get_object()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return self.partial_update(request, *args, **kwargs)


class DeleteProfile(DestroyAPIView):
    permission_classes = (IsAuthenticated,IsUser,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class FollowersList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.request
        kwargs['page'] = 'followers'
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        self.user_profile=  Profile.objects.get(id = self.kwargs['pk'])
        if self.user_profile.id != self.request.user.id and  self.user_profile.private:
            return None
        return self.user_profile.following.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset and self.user_profile.private:
            return Response({'detail':'Profile is private'},status=status.HTTP_403_FORBIDDEN)
        elif not queryset:
            return Response({'detail':'No Followers'})

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return  Response(serializer.data)


class FollowingList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.request
        kwargs['page'] = 'following'
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        self.user_profile=  Profile.objects.get(id = self.kwargs['pk'])
        if self.user_profile.id != self.request.user.id and  self.user_profile.private:
            return None
        return self.user_profile.follower.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if not queryset and self.user_profile.private:
            return Response({'detail':'Profile is private'},status=status.HTTP_403_FORBIDDEN)
        elif not queryset:
            return Response({'following': None})

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return  Response(serializer.data)


class FollowUser(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.request
        kwargs['page'] = None
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(following = self.following, follower = self.request.user.profile)

    def create(self, request, *args, **kwargs):
        self.following = Profile.objects.get(id =self.kwargs['pk'])
        if self.following == self.request.user.profile:
            return  Response({'Invalid':"Can't follow Yourself"},status.HTTP_406_NOT_ACCEPTABLE)
        try:
            Follow.objects.get(following = self.following, follower = self.request.user.profile)
            return Response({'Invalid':"Already following"},status=status.HTTP_400_BAD_REQUEST)
        except:
            return super().create(request, *args, **kwargs)        


class UnFollow(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowSerializer

    def get_object(self):
        follower = self.request.user.profile
        following = Profile.objects.get(id =self.kwargs['pk'])
        if follower == following:
            return None
        try:
            return Follow.objects.get(following =following , follower = follower)
        except:
            raise Http404

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.request
        kwargs['page'] = None
        return super().get_serializer(*args, **kwargs)


class Timeline(ListAPIView):
    permission_classes = (IsAuthenticated,ValidUser,)
    serializer_class = BlogSerializer 
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        following = self.request.user.profile.follower.all()
        blog_list = (Blog.objects.filter(writer = f.following) for f in following)
        try:
            first = next(blog_list)
            blog_query = first.union(*blog_list).order_by('-created')
        except:
            blog_query =None
        return blog_query

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] ={'page':'profile'}
        return super().get_serializer(*args, **kwargs)
from rest_framework.permissions import   IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status  
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView,RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView


from api.perm import IsBlogUser, IsNotBlogUser
from blogs.models import Blog, Review, Tag
from ..serializers import BlogSerializer, RelatedBlogSerializer, ReviewSerializer, TagSerializer

@api_view(['GET','POST'])
def get_routes(request):

    routes= [
        {['GET']:'api/'},
        {['GET']:'api/blogs/'},
        {['POST']:'api/blog/create/'},
        {['GET']:'api/blog/<str:pk>/view/'},
        {['GET','PATCH','PUT']:'api/blog/<str:pk>/update/'},
        {['DELETE']:'api/blog/<str:pk>/delete/'},
        {['POST']:'api/blog/<str:pk>/vote/'},
        {['GET']:'api/blog/<str:pk>/reviews/'},
        {['GET']:'api/tags/'},
        {['POST']:'api/tag/create/'},
        {['GET']:'api/tag/<str:pk>/'},
        {['DELETE']:'api/tag/<str:pk>/delete'},
        {['POST']:'api/token/'},
        {['GET']:'api/users/'},
        {['POST']:'api/users/create/'},
        {['GET']:'api/users/profile/<str:pk>/'},
        {['GET','PATCH','PUT']:'api/users/profile/<str:pk>/update/'},
        {['DELETE']:'api/users/profile/<str:pk>/delete/'},
        {['GET']:'api/users/profile/<str:pk>/followers/'},
        {['GET']:'api/users/profile/<str:pk>/following/'},
        {['POST',]:'api/users/profile/<str:pk>/follow/'},
        {['DELETE']:'api/users/profile/<str:pk>/unfollow/'},
    ]

    return Response(routes)


class CreateBlog(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_serializer_context(self):
        context= super().get_serializer_context()
        context['page'] = 'create'
        return context

    def perform_create(self, serializer):
        serializer.save(writer = self.request.user.profile)


class GetBlogs(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class ViewBlog(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        
        rel_blog_list = []
        for tag in resp.data['tags']: 
            tag_obj =  Tag.objects.get(name = tag[1:])
            rel_blogs = list(tag_obj.blog_set.exclude(title =resp.data['title']).order_by('-vote_total')[:3])
            rel_blog_list += [blog for blog in rel_blogs if blog not in rel_blog_list]
                
        sorted(rel_blog_list ,key=lambda x: x.vote_count)
        ser =RelatedBlogSerializer(rel_blog_list ,many =True)
        resp.data['related_blogs'] =ser.data
        return Response(resp.data ,status =status.HTTP_200_OK)


class UpdateDetailBlog(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,IsBlogUser,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] ={'page':'update'}
        return super().get_serializer(*args, **kwargs)


class DeleteBlog(DestroyAPIView):
    permission_classes = (IsAuthenticated,IsBlogUser,)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class AddReview(CreateAPIView):
    permission_classes = (IsAuthenticated,IsNotBlogUser,)
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blog = Blog.objects.get(id = self.kwargs['pk'])
        serializer.save(owner = self.request.user.profile,blog = blog)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ReviewList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return  Review.objects.filter(blog__id = self.kwargs['pk'] )


# Tags Block
class TagList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ViewTag(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CreateTag(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer


class DeleteTag(DestroyAPIView):
    permission_classes = (IsAuthenticated,IsAdminUser)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

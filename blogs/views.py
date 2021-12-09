from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from blogs.forms import BlogForm, ImageForm, ReviewForm
from .models import Blog, Image, Review


# Create your views here.
def home(request):
	blogs = Blog.objects.all().order_by('-vote_ratio','-vote_total')
	context = {'blogs': blogs[:3], 'request': request }
	return render(request , 'blogs/home.html',context) 

@login_required(login_url= 'login_user')
def add_blog(request):
	form = BlogForm()

	if request.method == 'POST':
		form = BlogForm(request.POST ,request.FILES)
		if form.is_valid():
			blog = form.save(commit=False)
			blog.writer = request.user.profile
			blog.save()
			form.save_m2m()
			id = blog.id
			return redirect('blog-images' , id)

	context = {'form': form}

	return render(request , 'blogs/blogform.html' ,context)

@login_required(login_url= 'login_user')
def view_blog(request, pk):
	blog  = Blog.objects.get(id = pk)
	rel_blogs = []
	for tag in blog.tags.all():
		b= Blog.objects.filter(tags = tag).exclude(id = blog.id).order_by('-vote_ratio','-vote_total')

		if b not in rel_blogs:
			rel_blogs += b 
	rel_blogs = set(rel_blogs)
	form =ReviewForm()

	if request.method == 'POST':
		form =ReviewForm(request.POST)
		rev = form.save(commit=False)
		rev.owner = request.user.profile
		rev.blog = blog
		rev.save()
		rev.get_vote_ratio
		return redirect('view-blog' , pk = pk)

	try:
		voted = Review.objects.get(blog = blog , owner =request.user.profile)
	except:
		voted =None
	context = {'blog' : blog ,'rel_blogs': rel_blogs ,'form': form, 'voted': voted}
	return render(request , 'blogs/blogpage.html' ,context)


@login_required(login_url= 'login_user')
def add_images(request , pk):
	
	blog  = Blog.objects.get(id = pk)
	form  = ImageForm()
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		b = form.save(commit= False)
		b.blog =blog
		b.save()
		form.save_m2m()
		return redirect('view-blog' , pk)
	
	context = {'form': form , 'id': blog.id}
	return render(request , 'blogs/imageform.html', context)


def all_blogs(request):
	blogs = Blog.objects.alias().order_by('created')
	context ={'blogs':blogs}
	return render(request , 'blogs/blogs_all.html', context)

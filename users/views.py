from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from blogs.models import Blog
from django.contrib.auth.decorators import login_required

from users.forms import ProfileForm, SignupForm
from .models import Follow, Profile
# Create your views here.

def login_user(request):
    page = 'login'
    user = None
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try :
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User name doesn't exist!")
            return redirect('login_user')

        user = authenticate(username = username , password = password)

        if user is not None:
            login(request, user) 
            return redirect('timeline')
        else:
            messages.error(request, 'Username/password is incorrect!')

    context = {'page': page}
           
    return render(request , 'login.html',context)

@login_required(login_url= 'login_user')
def logout_user(request):
    logout(request)
    messages.success(request,'Logged out Succesfully!!')
    return redirect('login_user')

def writers(request):
    profiles = Profile.objects.all()
    cur_user=None
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(id = request.user.profile.id)
        cur_user = request.user.profile
    context = {'profiles': profiles , 'cur_user': cur_user}
    return render(request , 'users/writers.html',context)

def register_user(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('home')
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        form.save()
        return redirect('home')
    context = {'page': page ,'form': form}
    return render(request , 'login.html', context)

@login_required(login_url= 'login_user')
def update_profile(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance =  profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST , request.FILES,instance =  profile)
        if form.is_valid():
            form.save()

        return redirect('home')
    return render(request , 'users/profileform.html' ,{'form': form})

@login_required(login_url= 'login_user')
def timeline(request):
    following  = request.user.profile.follower.all()
    blogs = []
    for f in following:
        blogs += Blog.objects.filter(writer = f.following).order_by('created')
    
    # blogs = Blog.objects.filter(writer = following).order_by('created')
    context ={'blogs':blogs}
    return render(request,'users/timeline.html',context)

@login_required(login_url= 'login_user')
def account(request ,pk):
    profile = Profile.objects.get(id =pk)

    try:
        logged_user = request.user.profile
    except:
        logged_user = None


    following = profile.follower.all()
    context = {'profile' : profile , 'following': following ,'logged_user': logged_user}
    return render(request, 'users/profile.html',context) 

@login_required(login_url= 'login_user')
def follow(request,pk):
    profile = request.user.profile
    following = Profile.objects.get(id =pk)
    connection = Follow.objects.create(follower= profile ,following =following ) 
    messages.success(request,f'You are following{connection.following}')
    return redirect(request.GET['next'] if 'next' in  request.GET else 'account',profile.id )

@login_required(login_url= 'login_user')
def unfollow(request,pk):
    profile = request.user.profile
    following = Profile.objects.get(id =pk)
    try:
        connection = Follow.objects.get(follower= profile ,following = following)
        connection.delete() 
        messages.success(request,f'unfollowed {connection.following} successfuly')
    except:
        pass
    return redirect(request.GET['next'] if 'next' in  request.GET else 'account',profile.id )


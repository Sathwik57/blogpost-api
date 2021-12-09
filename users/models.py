from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import constraints

from django.db.models.constraints import UniqueConstraint



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , null= True ,blank= True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=100, unique=True)
    avatar = models.ImageField(default= 'default.jpg',null = True ,blank = True , upload_to = 'profileimages')
    intro = models.CharField(max_length=250, null=True ,blank=True)
    bio = models.TextField(null=True,blank=True)
    social_twitter = models.CharField(max_length=100, blank= True ,null= True)
    social_insta = models.CharField(max_length=100, blank= True ,null= True)
    private = models.BooleanField(default= False)
    created = models.DateField(auto_now_add= True)
    id = models.UUIDField(default = uuid.uuid4 , primary_key= True ,unique= True ,editable= False)

    def __str__(self) -> str:
        return self.username.title()

    def followers_count(self) :
        return self.following.all().count()

    def followers_list(self) :
        return self.following.all()

    def following_count(self) :
        return self.follower.all().count()
    
    def following_list(self) :
        return self.follower.all()
    
    def blog_count(self):
        return self.blog_set.all()

    @property
    def image_url(self):
        try:
            url = self.avatar.url
        except:
            url = '/images/default.jpg'
        return url


class Follow(models.Model):
    follower = models.ForeignKey(Profile , on_delete=models.CASCADE, related_name = 'follower')
    following = models.ForeignKey(Profile , on_delete=models.CASCADE, related_name = 'following')


    created = models.DateField(auto_now_add= True)

    class Meta:
        constraints = [
        UniqueConstraint(fields=['follower' , 'following'] , name='unique_followers'),
        ]
    def __str__(self) -> str:
        return f'{self.follower} follows {self.following}'





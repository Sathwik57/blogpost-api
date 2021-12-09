from django.db import models
import uuid

from django.db.models import constraints
from users.models import Profile
# from django.utils import timezone

# Create your models here.

class related_blogs(models.Manager):
    def get_blogs(self, tag):
        return self.filter(tags__name = tag)

class Blog(models.Model):
    
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE, null= True, blank= True)
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150 , null= True ,blank= True)
    post = models.TextField(null= True , blank= True)
    feature_image = models.ImageField(default = 'pattern.jpg' ,null =True ,blank = True , upload_to = 'uploaded')
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(null=True ,blank = True)
    vote_ratio = models.FloatField(null=True,blank=True) 


    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=  True)
    id = models.UUIDField(default= uuid.uuid4 , unique= True ,
                     primary_key= True , editable= False) 

    
    
    objects = models.Manager()
    related = related_blogs()

    def __str__(self) -> str:
        return self.title
    
    @property
    def get_vote_ratio(self):
        reviews = self.review_set.all()
        upvotes = reviews.filter(value = 'up').count()
        totalvotes = reviews.count()

        self.votes_total = upvotes
        self.votes_ratio = (upvotes/totalvotes) * 100 
        self.save()
        
    @property
    def image_url(self):
        try:
            url = self.feature_image.url
        except:
            url = '/images/pattern.jpg'
        return url

    @property
    def vote_count(self):
        if not self.vote_total:
            return 0
        return self.vote_total

class Tag(models.Model):
    name = models.CharField(max_length=50, unique= True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default= uuid.uuid4 , unique= True ,
                     primary_key= True , editable= False) 
                    
    def __str__(self) -> str:
        return '#'+self.name

class Image(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    image_x = models.ImageField(null =True ,blank = True , upload_to = 'uploaded') 
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default= uuid.uuid4 , unique= True ,
                     primary_key= True , editable= False) 


class Review(models.Model):
    VOTE = (
        ('up' , 'Like'),
        ('down' , 'Dislike'),
    )
    owner = models.ForeignKey(Profile, on_delete= models.CASCADE,null=True)
    blog = models.ForeignKey(Blog , on_delete=models.CASCADE)
    body = models.TextField(null = True , blank= True)
    value  = models.CharField(max_length=100, choices= VOTE)
    create = models.DateTimeField(auto_now_add = True) 
    id = models.UUIDField(default= uuid.uuid4 , unique= True, 
                          primary_key= True ,editable= False)

    class META:
        constraints = [
            constraints.UniqueConstraint(fields= ['owner' , 'blog'] ,name= 'unique_review')
        ] 

    def __str__(self) -> str:
        return self.value + '-' +self.blog.title
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import fields
from rest_framework.fields import empty
from rest_framework.permissions import SAFE_METHODS
from blogs.models import Blog, Review,Tag
from users.models import Follow, Profile

class UserSerializer(serializers.ModelSerializer):
    Reenter_password = serializers.CharField(
        max_length = 100,required =True,
        help_text='Enter the same password as before, for verification',
        write_only = True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'email' , 'username' , 'password','Reenter_password',]

    def validate(self, attrs):
        pswd1 =attrs['password']
        pswd2 = attrs['Reenter_password']
        if len(pswd1) < 8:
            raise serializers.ValidationError("Password must be atleast 8 characters") 
        elif pswd1 != pswd2 :
            raise serializers.ValidationError("Both Passwords must match")
        else:
            print(attrs)   
        return attrs

    def create(self, validated_data):
        validated_data.pop('Reenter_password')
        instance = User.objects.create(**validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
         
class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        exclude = ['user',]

    def get_name(self,obj):
        if not obj.name:
            return obj.username.title()
        return obj.name 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    writer = ProfileSerializer( read_only = True)

    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['vote_total', 'vote_ratio',]

    def __init__(self, instance=None, data=empty, **kwargs):
        try:
            page = kwargs['context'].pop('page')
            if page == 'profile':
                self.fields['writer'] = serializers.StringRelatedField() 
                self.fields['tags'] = serializers.StringRelatedField(many= True)
        except KeyError:
            self.fields['tags'] = serializers.StringRelatedField(many= True)
            
        super().__init__(instance=instance, data=data, **kwargs)

class RelatedBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title' ,'post','writer']

class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True ,required =False)
    class Meta:
        model = Review
        fields = ('owner','value','body',)

class FollowSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField(source = 'get_created',label = 'Following from',default = None)
    class Meta:
        model = Follow
        fields = ['created',]

    def get_created(self,obj):
        return obj.created

    def __init__(self, instance=None, data=empty, **kwargs):
        try:
            page = kwargs.pop('page')
        except:
            pass
        super().__init__(instance=instance, data=data, **kwargs)
        request = self.context

        if request.method in SAFE_METHODS:
            if page == 'followers':
                self.fields['follower'] = serializers.StringRelatedField()
            else:
                self.fields['following'] = serializers.StringRelatedField()

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)
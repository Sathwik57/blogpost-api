from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save , sender = User)
def profile_created(sender, instance ,created , **kwargs):
    user = instance
    if created:
        profile = Profile.objects.create(
            user = user,
            name = user.first_name,
            email = user.email,
            username = user.username
        )

@receiver(post_save ,sender = Profile)
def profile_updated(sender, instance ,created , **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.username = profile.username
        user.first_name = profile.name
        user.email = profile.email
        user.save()

@receiver(post_delete ,sender = Profile)
def profile_deleted(sender, instance  , **kwargs):
    profile = instance
    try:
        user = profile.user
        user.delete()
    except:
        pass

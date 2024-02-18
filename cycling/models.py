from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(
        User, related_name="post", 
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    post_image_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_like", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"{self.user}"
            f"({self.created_at:%Y-%m-%d %H:%M}):"
            f"{self.body}..."
        ) 

class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="comments", 
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="comments", 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.post} at {self.created_at:%Y-%m-%d %H:%M}"

class Profile(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 follows = models.ManyToManyField("self", 
        related_name="followed_by",
        symmetrical=False,
        blank=True)
 date_modified = models.DateTimeField(auto_now=True)
 profile_image_url = models.URLField(null=True, blank=True)
 profile_bio = models.CharField(null=True, blank=True, max_length=500)
 facebook_link = models.CharField(null=True, blank=True, max_length=100)
 homepage_link = models.CharField(null=True, blank=True, max_length=100)
 instagram_link = models.CharField(null=True, blank=True, max_length=100)
 linkedin_link = models.CharField(null=True, blank=True, max_length=100)
 
 def __str__(self):
        return self.user.username
 
 
 
 #Create Profile When New User Sings up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)

class City(models.Model):
    name= models.CharField(max_length=50)

    def __str__ (self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'
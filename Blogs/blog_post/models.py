from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# User = settings.AUTH_USER_MODEL


class Blogpost(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)    # CASCADE delete everything related to user when user delete his/her account
    title = models.CharField(max_length=120)                                # 'models.SET_NULL'  this is opposite of cascade, add 'null = True' ,if using this
    slug = models.SlugField(unique=True)
    image = models.ImageField(default='default_pic.jpg',upload_to='image/', null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:      # this will order the blogs with recent publish_date -> updated -> timestamp
        ordering = ['-publish_date', '-updated', '-timestamp']


class Querysearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    query = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)


class Commentsblog(models.Model):
    blogs = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    user = models.CharField(default="unknown", max_length=120)
    comment = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:      # this will order the blogs with recent publish_date -> updated -> timestamp
        ordering = ['-publish_date', '-updated', '-timestamp']



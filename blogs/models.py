from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    data_created = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    users_by_read = models.ManyToManyField(User, related_name='read_posts')


class Blog(models.Model):
    user_owner = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name='subscribed_blogs')

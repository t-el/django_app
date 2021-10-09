from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your models here.
class Article(models.Model):
    title = models.TextField(max_length=300)
    body = models.TextField()
    time = models.TimeField(auto_now=True)
    img = models.TextField(default="")
    tags = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.TextField(max_length=300)
    body = models.TextField()
    time = models.TimeField(auto_now=True)
    img = models.ImageField(null=True)
    tags = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title


class Profile(models.Model):
    img = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.TextField(max_length=50)
    location = models.TextField(max_length=50, blank=True, null=True, default="")
    company = models.TextField(max_length=50, blank=True, null=True, default="")
    about = models.TextField(max_length=400, null=True)
    statu = models.IntegerField(default=1)
    since = models.DateField(auto_now_add=True, null=True)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.fullname


class Relation(models.Model):
    statu = models.CharField(max_length=4, null=True)
    since = models.DateField(auto_now_add=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user", null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user", null=True)
    profile = models.ForeignKey(Profile, related_name="profile",on_delete=models.DO_NOTHING,null=True)
    class Meta:
        verbose_name_plural = "Relations"

    def __str__(self):
        return str(self.since)

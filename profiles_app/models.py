from django.db import models
from django.contrib.auth.models import User
from .utils import *
from django.template.defaultfilters import slugify


class Profile(models.Model):
    first_name = models.CharField(max_length=250, blank = True)
    last_name = models.CharField(max_length=250, blank = True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length=250, blank=True)
    email = models.EmailField(max_length=250, blank=True)
    image = models.ImageField(default="default.png", upload_to="images/")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)


    def __str__(self):
        return f"{self.user.username} - {self.created.strftime('%d-%m-%Y')}"


    def get_all_friends(self):
        return self.friends.all()


    def get_all_friends_number(self):
        return self.friends.all().count()


    def get_all_posts(self):
        return self.posts.all()


    def get_all_posts_number(self):
        return self.posts.all().count()


    def get_likes_given_number(self):
        likes = self.like_set.all()
        total_likes = 0
        for like in likes:
            if like.value == "like":
                total_likes += 1
        return total_likes


    def get_likes_received_number(self):
        posts = self.posts.all()
        total_likes = 0
        for post in posts:
            total_likes += post.liked.all().count()
        return total_likes


    def save(self, *args, **kwargs):
        ex = False
        to_slug = ""
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            ex = Profile.objects.filter(slug = to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug = to_slug).exists()
        else:
            to_slug = str(self.user.username)
        self.slug = to_slug
        super().save(*args, **kwargs)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")
    status_choices = (
        ("request", "request"), 
        ("accepted", "accepted")
    )
    status = models.CharField(max_length=10, choices=status_choices)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{self.sender} {self.status}ed {self.receiver} on {self.created.strftime('%d-%m-%Y')}"
from django.db import models
from profiles_app.models import Profile
from django.core.validators import FileExtensionValidator

# Create your models here.

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to="posts", blank=True, null = True)
    liked = models.ManyToManyField(Profile, blank=True, related_name="likes")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created", )


    def __str__(self):
        return f"{self.content[:20]}"


    def num_comments(self):
        return self.comment_set.all().count()


    def num_comments_(self):
        return self.comment_set.all()
        

    def num_likes(self):
        return self.liked.all().count()


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user}"

LIKE_CHOICES = (
    ("like", "like"),
    ("unlike", "unlike"),
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.value} {self.post}"
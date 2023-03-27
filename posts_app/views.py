from django.shortcuts import render
from .models import *


def main_posts_view(request):
    posts = Post.objects.all()

    context = {
        "posts":posts
    }
    return render(request, "posts_app/main.html", context)
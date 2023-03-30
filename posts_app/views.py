from django.shortcuts import *
from .models import *


def main_posts_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.filter(user = request.user).first()
    # comments = Comment.objects.all()
    if request.method == "POST" and "submit_post" in request.POST:
        content = request.POST["content"]
        if not request.POST["image"] == "":
            image = request.FILES["image"]
        else:
            image=None
        post = Post(content = content, user=profile, image=image)
        post.save() 

    if request.method == "POST" and "submit_comment" in request.POST:
        comment = request.POST["comment"]
        post_id = request.POST["post_id"]
        post_obj = Post.objects.filter(id = post_id).first()
        comment = Comment(user=profile, post=post_obj, body=comment)
        comment.save()
        
    context = {
        "posts":posts,
        "profile":profile
    }
    return render(request, "posts_app/main.html", context)


def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.filter(id = post_id).first()
        profile = Profile.objects.get(user = user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post=post_obj)

        if not created:
            if like.value=="Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        else:
            like.value="Like"

        post_obj.save()
        like.save()
    return redirect(request.META.get("HTTP_REFERER"))
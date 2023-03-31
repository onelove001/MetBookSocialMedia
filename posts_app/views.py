from django.shortcuts import *
from .models import *
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages


def main_posts_view(request):
    posts = Post.objects.all()
    profile = Profile.objects.filter(user = request.user).first()
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


def update_view(request, post_id):
    try:
        post = Post.objects.get(id = post_id)
        if request.user == post.user.user:
            if request.method == "POST":
                body = request.POST["body"]
                post.content = body
                post.save()
                return redirect("posts:post-view")
        else:
            messages.warning(request, "You are not authorize to edit this post")
            return redirect("posts:post-view")
    except:
        return redirect("posts:post-view")
    context = {"post":post}
    return render(request, "posts_app/update.html", context)


class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts_app/confirm_del.html"
    success_url = reverse_lazy("posts:post-view")

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        obj = Post.objects.get(pk = pk)
        if not obj.user.user == self.request.user:
            messages.warning(self.request, "You are not authorized to delete this post")
        return obj



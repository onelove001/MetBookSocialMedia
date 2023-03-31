from django.urls import path
from .views import *

app_name = "posts"


urlpatterns = [
    # Main Post Urls 

    path("", main_posts_view, name="post-view"),
    path("like_unlike", like_unlike_post, name="like-unlike"),
    path("<pk>/delete", PostDeleteView.as_view(), name="delete-post"),
    path("<post_id>/update", update_view, name="update-post"),

]
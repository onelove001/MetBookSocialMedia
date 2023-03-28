from django.urls import path
from .views import *

app_name = "posts"


urlpatterns = [
    # Main Post Urls 

    path("", main_posts_view, name="post-view"),
    path("like_unlike", like_unlike_post, name="like-unlike"),

]
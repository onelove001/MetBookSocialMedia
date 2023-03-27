from django.urls import path
from .views import *

app_name = "api"


urlpatterns = [
    # Api Urls
    path("user_profile", UserProfileApi.as_view(), name = "user-profile-api"),

]
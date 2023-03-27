from django.urls import path
from .views import *

app_name = "profiles"


urlpatterns = [
    # Main Profile Urls 
    path("user_profile", user_profile, name="user-profile"),

]
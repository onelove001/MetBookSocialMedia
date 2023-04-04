from django.urls import path
from .views import *

app_name = "profiles"


urlpatterns = [
    # Main Profile Urls 
    path("user_profile", user_profile, name="user-profile"),
    path("my_invites", invites_received_view, name="invites-received-view"),
    # path("list_profile", profile_list_view, name="list-profile"),
    path("list_profile", ProfileListView.as_view(), name="list-profile"),
    path("invite_available_list", invite_available_list, name="invite-available-list"),

    

]
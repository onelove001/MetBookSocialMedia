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
    path("send_invite", send_invitation, name="send-invitation"),
    path("remove_from_friends", remove_from_friends, name="remove-friend"),
    path("accept_friend", accept_invitation, name="accept-request"),
    path("reject_friend", reject_invitation, name="reject-request"),
 

]
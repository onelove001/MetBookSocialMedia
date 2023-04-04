from django.shortcuts import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import *
from django.views.generic import ListView
from django.contrib.auth.models import User


# Main Views
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            bio = request.POST.get("bio")
            if request.FILES.get("image", False):
                image = request.FILES['image']
                fs = FileSystemStorage()
                profile_image_save = fs.save(image.name, image)
                image_url = fs.url(profile_image_save)
            else:
                image_url = None

            profile.first_name = first_name
            profile.last_name = last_name
            profile.bio = bio
            if image_url != None:
                profile.image = image_url
            profile.save()
            messages.success(request, "Profile Updated!")
            return redirect(request.META.get("HTTP_REFERER"))
        except:
            messages.error(request, "Failed To Update!")

    context = {"profile":profile}
    return render(request, "profiles_app/my_profile.html", context)


def invites_received_view(request):
    profile = Profile.objects.get(user = request.user)
    qs = Relationship.objects.invitations_received(profile) 

    context = {"qs":qs}
    return render(request, "profiles_app/my_invites.html", context)


def invite_available_list(request):
    user = request.user
    qs = Profile.objects.all_profiles_available(user)

    context = {"qs":qs}
    return render(request, "profiles_app/invite_available_list.html", context)


# def profile_list_view(request):
#     user = request.user
#     qs = Profile.objects.get_all_profiles(user)

#     context = {"qs":qs}
#     return render(request, "profiles_app/list_profile.htm", context)


class ProfileListView(ListView):
    model = Profile
    template_name = "profiles_app/list_profile.htm"
    context_object_name = "qs"

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user = user)
        rel_s = Relationship.objects.filter(receiver = profile)
        rel_r = Relationship.objects.filter(sender = profile)
        rel_receiver = []
        rel_sender = []

        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        
        context["is_empty"] = False
        if len(self.get_queryset()) == 0:
            context["is_empty"] = True
        return context
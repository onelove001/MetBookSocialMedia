from django.shortcuts import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import *
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q


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
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {"qs":results, "is_empty":is_empty}
    return render(request, "profiles_app/my_invites.html", context)


def accept_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(pk = pk)
        receiver = Profile.objects.get(user = request.user)
        rel = get_object_or_404(Relationship, sender = sender, receiver = receiver)
        if rel.status == "request":
            rel.status = "accepted"
            rel.save()
    return redirect("profiles:invites-received-view")


def reject_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        sender = Profile.objects.get(pk = pk)
        receiver = Profile.objects.get(user = request.user)
        rel = get_object_or_404(Relationship, sender = sender, receiver = receiver)
        if rel.status:
            rel.delete()
    return redirect("profiles:invites-received-view")


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


def send_invitation(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        user = request.user
        sender = Profile.objects.get(user = user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.create(sender=sender, receiver=receiver, status="request")
        rel.save()
        return redirect(request.META.get("HTTP_REFERER"))
    return redirect("profiles:user-profile")


def remove_from_friends(request):
    if request.method == "POST":
        pk = request.POST.get("profile_pk")
        user = request.user
        sender = Profile.objects.get(user = user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | Q(sender=receiver) & Q(receiver=sender))
        rel.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    return redirect("profiles:user-profile")
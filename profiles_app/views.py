from django.shortcuts import *
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import *
import requests


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

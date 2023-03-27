from django.shortcuts import *


def home(request):
    user = request.user
    context = {"user":user}
    return render(request, "index.html", context)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from profiles_app.views import *

urlpatterns = [
    
    path("admin/", admin.site.urls),
    path("profiles/", include("profiles_app.urls", namespace="profiles")),
    path("posts/", include("posts_app.urls", namespace="posts")),
    path("api/", include("Api.urls", namespace="api")),
    path("", home, name="home"),

]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
from django.shortcuts import render
from profiles_app.models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# Profile Api(s) Views

class UserProfileApi(APIView):
    """ 
    Shows User Profile Details 
    """

    def get(self, request, format=None):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

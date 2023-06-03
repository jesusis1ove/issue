import rest_framework.permissions
from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserInfoView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)





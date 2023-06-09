import rest_framework.pagination
from django.db.models import F
from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from .models import Issue, Comment, Notification
from .pagination import CustomPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .services.issues_services import *


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['owner', 'is_active', 'created_at']
    search_fields = ['title']
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.IssueListSerializer
        return serializers.IssueSerializer

    def get_queryset(self):
        queryset = Issue.objects.all().order_by('-created_at')

        sort_by = self.request.query_params.get('sort_by')
        sort_dir = self.request.query_params.get('sort_dir')

        if sort_by is not None:
            ordering_str = F(sort_by).desc()
            if sort_dir == 'asc':
                ordering_str = F(sort_by).asc()
            queryset = queryset.order_by(ordering_str, 'id')

        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        data['owner'] = request.user.id
        attachments = request.FILES.getlist('file', None)

        serializer = self.get_serializer(data=data, context={'attachments': attachments})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['issue']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CommentListSerializer
        return serializers.CommentSerializer


class NotificationView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.NotificationSerializer

    def get_queryset(self):
        subscribed_issues = Issue.objects.filter(subscribers=self.request.user)
        return Notification.objects.filter(issue__in=subscribed_issues)





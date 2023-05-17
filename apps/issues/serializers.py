from rest_framework import serializers

from apps.accounts.serializers import UserSimpleSerializer
from .models import Issue, Comment, Label


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class IssueListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d')
    owner = UserSimpleSerializer()
    comment_count = serializers.IntegerField()

    class Meta:
        model = Issue
        fields = ('id', 'title', 'owner', 'comment_count', 'is_active', 'created_at', 'updated_at')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'
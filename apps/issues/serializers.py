from rest_framework import serializers

from apps.accounts.serializers import UserSimpleSerializer
from .models import Project, Issue, IssueAttachment, Comment, Notification


class IssueSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        attachments = self.context['attachments']
        issue = Issue.objects.create(**validated_data)
        for attachment in attachments:
            IssueAttachment.objects.create(issue=issue, file=attachment)
        return issue

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['attachments'] = IssueAttachmentSerializer(instance.get_attachments(), many=True).data
        return representation

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


class IssueAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueAttachment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'owner': {'default': serializers.CurrentUserDefault()}}


class CommentListSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

from django.contrib import admin

from .models import Project, Issue, IssueSubscriber, IssueAttachment, Comment, Notification


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(IssueSubscriber)
class IssueSubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'subscriber')


class IssueSubscribersInline(admin.TabularInline):
    model = IssueSubscriber


class IssueAttachmentInLine(admin.TabularInline):
    model = IssueAttachment


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    inlines = (IssueSubscribersInline, IssueAttachmentInLine)
    list_display = ('id', 'title', 'owner', 'created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'owner', 'created_at', 'updated_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'type')
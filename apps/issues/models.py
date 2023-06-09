from django.db import models
from django_issues.settings import AUTH_USER_MODEL


class Project(models.Model):
    name = models.CharField(max_length=200)


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscribers = models.ManyToManyField(AUTH_USER_MODEL, related_name='subscribers', through='IssueSubscriber')

    @property
    def comment_count(self):
        return Comment.objects.filter(issue=self).count()

    def get_attachments(self):
        return IssueAttachment.objects.filter(issue=self).all()

    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'


class IssueAttachment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/%Y/')


class IssueSubscriber(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('comment', 'new comment'),
        ('issue', 'issue has been updated'),
    )
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def mark_as_viewed(self):
        self.is_viewed = True
        self.save()





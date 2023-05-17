from django.db import models
from django_issues.settings import AUTH_USER_MODEL


class Issue(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def comment_count(self):
        return Comment.objects.filter(issue=self.id).count()

    class Meta:
        verbose_name = 'issue'
        verbose_name_plural = 'issues'


class Label(models.Model):
    label = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'label'
        verbose_name_plural = 'labels'


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


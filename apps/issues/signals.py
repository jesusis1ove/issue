from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification, Comment, Issue


@receiver(post_save, sender=Comment)
def create_notify(sender, instance, created, **kwargs):
    if created:
        for user in instance.issue.subscribers.all():
            notification = Notification.objects.create(issue=instance.issue,
                                                       user=user,
                                                       type='comment')
            notification.save()

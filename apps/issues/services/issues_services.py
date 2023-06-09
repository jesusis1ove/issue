from ..models import Issue, Notification


def get_issue_subscribers(issue:Issue):
    pass


def notifications_is_viewed_by_user(user):
    user_notifications = Notification.objects.filter(user=user)
    [notification.viewed() for notification in user_notifications]


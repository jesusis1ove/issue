from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('issues', IssueViewSet, basename='issue')
router.register('comments', CommentViewSet, basename='comment')
#router.register('comments', CommentViewSet, basename='comment')

urlpatterns = router.urls

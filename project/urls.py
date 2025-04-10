from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project.views import IssueViewSet, CommentViewSet, ProjectViewSet

router = DefaultRouter()
router.register('project', ProjectViewSet, basename='project')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls), name='project'),
    ]

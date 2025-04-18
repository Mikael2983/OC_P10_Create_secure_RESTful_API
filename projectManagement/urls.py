from rest_framework.routers import DefaultRouter

from projectManagement.views import (
    IssueViewSet, CommentViewSet, ProjectViewSet
)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("issues", IssueViewSet, basename="issue")
router.register("comments", CommentViewSet, basename="comment")

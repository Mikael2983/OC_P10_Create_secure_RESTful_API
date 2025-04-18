from rest_framework.routers import DefaultRouter

from project.views import IssueViewSet, CommentViewSet, ProjectViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("issues", IssueViewSet, basename="issue")
router.register("comments", CommentViewSet, basename="comment")

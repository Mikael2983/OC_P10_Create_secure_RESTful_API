from rest_framework.permissions import BasePermission, SAFE_METHODS

from project.models import Issue, Project, Comment


class IsAuthor(BasePermission):
    """
    Grants modification and deletion rights only to the object's author.
    """

    def has_object_permission(self, request, view, obj):
        """
        - Safe methods: always allowed.
        - Unsafe methods: allowed only if user is the author.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsContributor(BasePermission):
    """
    Grants access to project contributors for reading and creating content.
    """

    @staticmethod
    def get_project_from_request(request, basename):
        if basename == "comment":
            issue_id = request.data.get("issue")
            return Issue.objects.get(id=issue_id).project
        if basename == "issue":
            project_id = request.data.get("project")
            return Project.objects.get(id=project_id)
        return None  # for other cases like project itself

    @staticmethod
    def get_project_from_object(obj):
        if isinstance(obj, Project):
            return obj
        if isinstance(obj, Issue):
            return obj.project
        if isinstance(obj, Comment):
            return obj.issue.project
        return None

    def has_permission(self, request, view):
        """
        - Allow listing for all authenticated users.
        - Require contributor status for creation (except project).
        """
        if view.action == "list":
            return True
        if view.action == "create" and view.basename != "project":
            project = self.get_project_from_request(request, view.basename)
            return project and project.contributors.filter(user=request.user).exists()
        return True

    def has_object_permission(self, request, view, obj):
        """
        - Read access allowed to contributors.
        """
        project = self.get_project_from_object(obj)
        return project and project.contributors.filter(user=request.user).exists()

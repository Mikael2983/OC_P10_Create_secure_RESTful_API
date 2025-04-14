from rest_framework.permissions import BasePermission, SAFE_METHODS

from project.models import Issue, Project, Comment

UNSAFE_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']


class IsAuthor(BasePermission):
    """
    - Allowed reading to project contributors.
    - Modification and deletion reserved to the author of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        - Read allowed if the user is a contributor to the project.
        - Modification/deletion allowed only to the author of the object.
        """

        if request.method in UNSAFE_METHODS:
            return obj.author == request.user  # Seul l’auteur peut modifier ou supprimer

        return True


class IsContributor(BasePermission):
    """
    - Only contributors to a project can see its details and create issues/comments.
    - Only the author can edit or delete a project, issue or comment.
    """

    @staticmethod
    def get_project_from_issue_id(request):
        issue_id = request.data.get("issue")
        issue = Issue.objects.get(id=issue_id)
        return issue.project

    @staticmethod
    def get_project_from_project_id(request):
        project_id = request.data.get("project")
        return Project.objects.get(id=project_id)

    @staticmethod
    def get_project_from_comment(item):
        return item.issue.project

    @staticmethod
    def get_project_from_issue(item):
        return item.project

    @staticmethod
    def get_project(item):
        return item

    GET_PROJECT = {
        "comment": get_project_from_issue_id,
        "issue": get_project_from_project_id
    }

    def has_permission(self, request, view):

        if view.action == "list":
            return True

        if view.action == "create":

            function_to_execute = self.GET_PROJECT[view.basename]
            project = function_to_execute(request)

            return project.contributors.filter(user=request.user).exists()

        return True

    def has_object_permission(self, request, view, obj):
        """
        - Lecture : Seuls les contributeurs du projet peuvent voir les détails.
        - Modification/Suppression : Réservée à l'auteur de l'objet.
        """

        mapping = {
            Project: self.get_project,
            Issue: self.get_project_from_issue,
            Comment: self.get_project_from_comment
        }

        function_to_execute = mapping.get(type(obj))
        project = function_to_execute(obj)

        is_contributor = project.contributors.filter(
            user=request.user).exists()
        is_author = obj.author == request.user

        if request.method in SAFE_METHODS:
            return is_contributor
        if request.method in UNSAFE_METHODS:
            return is_author

        return False

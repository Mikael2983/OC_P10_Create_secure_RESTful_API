from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from project.models import Project, Issue
from project.permissions import IsContributor
from project.serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter projects to return only those where the user is a contributor or author.
        """
        queryset = (Project.objects.filter(contributors=self.request.user) |
                    Project.objects.filter(author=self.request.user)
                    )

        return queryset


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        """
        Filter issues to return only those where the user is a contributor or author.
        """
        queryset = Issue.objects.all()
        project_id = self.request.GET.get('project_id')
        if project_id:
            queryset = queryset.filter(projet_id=project_id)
        return queryset


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsContributor]

    def get_queryset(self):
        queryset = Issue.objects.all()
        issue_id = self.request.GET.get('issue_id')
        if issue_id:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from authenticated.models import User
from project.models import Project, Issue, Contributor, Comment
from project.permissions import IsContributor, IsAuthor
from project.serializers import (
    ProjectListSerializer, CommentSerializer, ContributorSerializer,
    ProjectDetailSerializer, IssueListSerializer, IssueDetailSerializer
)


class MultipleSerializerMixin:
    """
    Allows you to use a different serializer for retail actions
    (retrieve, create, update, partial_update) in a ViewSet.
    """
    detail_serializer_class = None

    def get_serializer_class(self):
        """
        Returns the appropriate serializer according to the action.
        """
        method = ['retrieve', 'create', 'update', 'partial_update']
        if self.action in method and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    ViewSet to manage projects. Allows:
    - list the projects whose user is a contributor,
    - create a project (automatically assigned to the author),
    - add or remove a contributor (if the user is the author).
    """
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

    def get_queryset(self):
        """
        Returns the list of projects where the user is a contributor.
        """
        return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer):
        """
        When creating a project, the author is automatically defined as the current user.
        """
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Do not use PUT. Use PATCH for updates.
        """
        if request.method == 'PUT':
            raise MethodNotAllowed("PUT")
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="add_contributor")
    def add_contributor(self, request, pk=None):
        """
        Adds a contributor to a project if the user is the author.
        """

        project = get_object_or_404(Project, pk=pk)

        if project.author != request.user:
            return Response(
                {
                    "error": "Seul l'auteur du projet peut ajouter un contributeur.",
                    "code": "author_only"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {
                    "error": "L'ID de l'utilisateur est requis.",
                    "code": "user_id_required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, pk=user_id)

        if Contributor.objects.filter(project=project, user=user).exists():
            return Response(
                {
                    "message": "Cet utilisateur est déjà contributeur du projet.",
                    "code": "already_contributor"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        Contributor.objects.create(project=project, user=user)

        return Response(
            {
                "message": f"L'utilisateur {user.username} a été ajouté comme contributeur.",
                "code": "contributor_added"
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["delete"], url_path="del_contributor")
    def remove_contributor(self, request, pk=None):
        """
        Removes a contributor from a project if the user is the author.
        """
        project = get_object_or_404(Project, pk=pk)

        if project.author != request.user:
            return Response(
                {
                    "error": "Seul l'auteur du projet peut retirer un contributeur.",
                    "code": "author_only"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {
                    "error": "L'ID de l'utilisateur est requis. format 'user_id': id",
                    "code": "user_id_required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, pk=user_id)

        if user == request.user:
            return Response(
                {
                    "error": "l'auteur ne peut être retirer des contributeurs",
                    "code": "cannot_remove_author"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        contributor = Contributor.objects.filter(project=project, user=user).first()
        if not contributor:
            return Response(
                {
                    "error": "Cet utilisateur n'est pas un contributeur du projet.",
                    "code": "not_a_contributor"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        contributor.delete()
        return Response(
            {
                "message": f"L'utilisateur {user.username} a été retiré du projet.",
                "code": "contributor_removed"
            },
            status=status.HTTP_201_CREATED
        )


class ContributorViewSet(ModelViewSet):
    """
    ViewSet to view user contributions.
    The user sees only his own contributions.
    """
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def get_queryset(self):
        """
        Filters contributions to those of the current user.
        """
        queryset = self.queryset.filter(user=self.request.user)
        return queryset


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    ViewSet to manage issues associated with project outcomes.
    Only contributors can view issues.
    Only author can edit issues.
    """
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

    def get_queryset(self):
        """
        Returns issues related to projects where the user is a contributor.
        """
        queryset = Issue.objects.filter(
            project__contributors__user=self.request.user)
        return queryset

    def update(self, request, *args, **kwargs):
        """
        Do not use PUT. Use PATCH for updates.
        """
        if request.method == 'PUT':
            raise MethodNotAllowed("PUT")
        return super().update(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    """
    ViewSet to manage comments associated with project outcomes.
    Only contributors can view comments.
    Only author can edit comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

    def get_queryset(self):
        """
        Returns comments related to projects where the user is a contributor.
        """
        queryset = Comment.objects.filter(
            issue__project__contributors__user=self.request.user)
        return queryset

    def update(self, request, *args, **kwargs):
        """
        Do not use PUT. Use PATCH for updates.
        """
        if request.method == 'PUT':
            raise MethodNotAllowed("PUT")
        return super().update(request, *args, **kwargs)

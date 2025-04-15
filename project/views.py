from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
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
    detail_serializer_class = None

    def get_serializer_class(self):
        method = ['retrieve', 'create', 'update', 'partial_update']
        if self.action in method and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

    def get_queryset(self):
        queryset = Project.objects.filter(contributors__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Assigner l'utilisateur authentifié comme auteur."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], url_path="add_contributor")
    def add_contributor(self, request, pk=None):
        """
        Adds a contributor to a specific project.
        Only the author of the project can add a contributor.
        """
        project = get_object_or_404(Project, pk=pk)

        # Check if the request user is the project Author
        if project.author != request.user:
            return Response(
                {
                    "error": "Seul l'auteur du projet peut ajouter un contributeur."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Retrieve the user to add (from sent data)
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "L'ID de l'utilisateur est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user exists
        user = get_object_or_404(User, pk=user_id)

        # Check if user is already contributor
        if Contributor.objects.filter(project=project, user=user).exists():
            return Response(
                {
                    "message": "Cet utilisateur est déjà contributeur du projet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add user as contributor
        Contributor.objects.create(project=project, user=user)

        return Response(
            {
                "message": f"L'utilisateur {user.username} a été ajouté comme contributeur."},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["Delete"], url_path="del_contributor")
    def remove_contributor(self, request, pk=None):
        """
        remove a contributor from a specific project.
        Only the author of the project can remove a contributor.
        """

        project = get_object_or_404(Project, pk=pk)

        # Check if the request user is the project Author
        if project.author != request.user:
            return Response(
                {
                    "error": "Seul l'auteur du projet peut retirer un contributeur."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Retrieve the user to add (from sent data)
        user_id = request.data.get("user_id")
        if not user_id:
            return Response(
                {"error": "L'ID de l'utilisateur est requis. format 'user_id': id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the user exists
        user = get_object_or_404(User, pk=user_id)

        if user == request.user:
            return Response(
                {"error": "l'auteur ne peut être retirer des contributeurs"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if user is a contributor
        contributor = get_object_or_404(Contributor, project=project, user=user)

        if not contributor:
            return Response(
                {
                    "message": "Cet utilisateur n'est pas un contributeur du projet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        contributor.delete()
        return Response(
            {
                "message": f"L'utilisateur {user.username} a été retiré du projet."},
            status=status.HTTP_201_CREATED
            )


class ContributorViewSet(ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset


class IssueViewSet(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

    def get_queryset(self):
        """
        Filter issues to return only those where the user is a contributor or author.
        """
        queryset = Issue.objects.filter(
                project__contributors__user=self.request.user)
        return queryset


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor, IsContributor]

    def get_queryset(self):
        queryset = Comment.objects.filter(
            issue__project__contributors__user=self.request.user)
        return queryset

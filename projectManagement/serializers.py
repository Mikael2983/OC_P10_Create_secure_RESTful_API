from rest_framework import serializers
from authenticated.serializers import UserListSerializer
from authenticated.models import User
from projectManagement.models import Comment, Issue, Project, Contributor


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a contributor to a project.
    Displays user information using the UserListSerializer.
    """

    user = UserListSerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = ["user"]


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments related to an issue.
    Provides details of the comment and the author and associated issue.
    """

    author = serializers.StringRelatedField(read_only=True)
    issue = serializers.PrimaryKeyRelatedField(
        queryset=Issue.objects.all(), allow_null=False
    )

    class Meta:
        model = Comment
        fields = ["id", "description", "date_created", "author", "issue"]

    def create(self, validated_data):
        """
        Creates a new comment by automatically associating
        the current user as author.
        """
        request = self.context.get("request")
        validated_data["author"] = request.user
        comment = Comment.objects.create(**validated_data)
        return comment


class IssueListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer to display a list of issues.
    Provides the main information of an issue.
    """

    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "title",
            "status",
            "date_created",
            "project",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for an issue.
    Displays all relevant information, including author,
    the assigned user, comments, and associated project.
    """

    author = serializers.StringRelatedField(read_only=True)
    assigned = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), allow_null=False)

    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "nature",
            "date_created",
            "author",
            "assigned",
            "project",
            "comments",
        ]

    @staticmethod
    def get_comments(instance):
        """
        Retrieves and serializes comments associated with this issue.
        """
        queryset = instance.issue_comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data

    def validate(self, data):
        """
        Validates that the assigned user is a contributor to the project.
        """
        assigned_user = data.get("assigned")
        project = data.get("project")
        if (
            assigned_user
            and not project.contributors.filter(user=assigned_user).exists()
        ):
            raise serializers.ValidationError(
                "L'utilisateur assigné doit être contributeur du projet."
            )
        return data

    def create(self, validated_data):
        """
        Creates an issue by automatically assigning the author to the current
        user.
        """
        request = self.context.get("request")
        validated_data["author"] = request.user
        issue = Issue.objects.create(**validated_data)
        return issue


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer for the list of projects.
    Provides essential information about a project.
    """

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "date_created",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a project.
    Includes information from the author, contributors and associated issues.
    Also allows adding contributors via a list of IDs.
    """

    author = serializers.StringRelatedField(read_only=True)

    contributors_info = ContributorSerializer(
        source="contributors", many=True, read_only=True
    )
    contributors_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    issues = IssueListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "author",
            "description",
            "type",
            "date_created",
            "contributors_info",
            "contributors_ids",
            "issues",
        ]

    def create(self, validated_data):
        """
        Creates a new project and assigns it to the current user as author.
        Also adds the contributors specified in `contributors_ids’.
        """
        request = self.context.get("request")
        validated_data.pop("author", None)  # delete the author field from data
        author = request.user
        contributor_ids = validated_data.pop("contributors_ids", [])

        # create project and re-define its author
        project = Project.objects.create(author=author, **validated_data)

        # Add author as contributor
        Contributor.objects.get_or_create(project=project, user=author)

        # Add the provided contributors (if they exist)
        for user_id in set(contributor_ids):
            user = User.objects.filter(id=user_id).first()
            if user:
                Contributor.objects.get_or_create(project=project, user=user)

        return project

import uuid

from django.db import models

from authenticated.models import User


class Contributor(models.Model):
    """
    Template representing a link between a user and a project as a contributor.
    A user can only be a contributor once per project.
    """

    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="contributors",
        blank=False, null=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contributed_projects",
        blank=False, null=False
    )

    class Meta:
        unique_together = ("project", "user")


class Project(models.Model):
    """
    Model representing a software project.
    A project has an author, type (backend, frontend, etc.), unique title and
    description.
    """

    TYPE_CHOICES = [
        ("back-end", "back-end"),
        ("front-end", "front-end"),
        ("iOS", "iOS"),
        ("Android", "Android"),
    ]
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255,
                             unique=True,
                             blank=False,
                             null=False)
    description = models.CharField(max_length=2550, blank=False, null=False)
    type = models.CharField(max_length=25,
                            choices=TYPE_CHOICES,
                            blank=False, null=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="authored_projects"
    )

    def __str__(self):
        return self.title


class Issue(models.Model):
    """
    Template representing an issue (bug, task or feature) associated with a
    project.

    Each issue includes:
    - a title,
    - a description,
    - a priority (Low, Medium, High),
    - a status (To Do, In Progress, Finished),
    - a nature (Bug, Feature, Task),
    - an author (creator of the issue),
    - an assigned user (optional),
    - a creation date.

    Constraint of uniqueness:
    - Issue title must be unique **within the same project**.
    """

    STATUS_CHOICES = [
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Finished", "Finished"),
    ]
    PRIORITY_CHOICES = [("Low", "low"), ("Medium", "Medium"), ("High", "High")]
    NATURE_CHOICES = [("Bug", "Bug"), ("Feature", "Feature"), ("Task", "Task")]

    title = models.CharField(max_length=255, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="issues_created"
    )

    assigned = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name="issues_assigned"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues",
        blank=False, null=False
    )

    description = models.CharField(max_length=2550, blank=False, null=False)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default="To Do",
                              blank=False, null=False)
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium",
        blank=False, null=False
    )
    nature = models.CharField(max_length=20, choices=NATURE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "project"], name="unique_issue_title_per_project"
            )
        ]


class Comment(models.Model):
    """
    Template representing comment made on issue.
    Each comment is linked to a specific author and issue.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="authored_comments"
    )
    description = models.CharField(max_length=255, blank=False, null=False)
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="issue_comments",
        blank=False, null=False
    )

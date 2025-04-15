import uuid

from django.db import models

from authenticated.models import User


class Contributor(models.Model):
    project = models.ForeignKey('Project',
                                on_delete=models.CASCADE,
                                related_name="contributors"
                                )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="contributed_projects"
                             )

    class Meta:
        unique_together = ('project', 'user')


class Project(models.Model):
    TYPE_CHOICES = [
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android')
    ]
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=2550)
    type = models.CharField(max_length=25, choices=TYPE_CHOICES)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_projects")

    def __str__(self):
        return self.title


class Issue(models.Model):
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]
    NATURE_CHOICES = [
        ('Bug', 'Bug'),
        ('Feature', 'Feature'),
        ('Task', 'Task')
    ]

    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="issues_created")

    assigned = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name="issues_assigned")

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues")

    description = models.CharField(max_length=2550)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='To Do'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='Medium'
    )
    nature = models.CharField(
        max_length=20,
        choices=NATURE_CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'project'],
                name='unique_issue_title_per_project'
            )
        ]


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_comments")
    description = models.CharField(max_length=255)
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name="issue_comments")

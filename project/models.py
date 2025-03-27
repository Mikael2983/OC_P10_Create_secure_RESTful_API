import uuid

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    can_be_contacted = models.BooleanField(null=True)
    can_data_be_shared = models.BooleanField(null=True)


class Project(models.Model):
    TYPE_CHOICES = [
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android')
    ]
    create_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2550)
    type = models.CharField(max_length=25, choices=TYPE_CHOICES)
    contributors = models.ManyToManyField(
        User,
        related_name="contributed_projects"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_projects")


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
    create_time = models.DateTimeField(auto_now_add=True)
    assigned = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_issues")

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=2550)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Todo'
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


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)

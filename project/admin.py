from django.contrib import admin
from django.contrib.admin import ModelAdmin
from project.models import Project, Issue, Comment, Contributor


class ProjectAdmin(ModelAdmin):

    list_display = [
        "id",
        "title",
        "description",
        "type",
        "author",
        "date_created",
    ]


class ContributorAdmin(ModelAdmin):
    list_display = [
        "id",
        "project",
        "user",
    ]


class IssueAdmin(ModelAdmin):
    list_display = [
        "id",
        "title",
        "author",
        "date_created",
        "assigned",
        "project",
        "description",
        "status",
        "priority",
        "nature",
    ]


class CommentAdmin(ModelAdmin):
    list_display = [
        "id",
        "date_created",
        "author",
        "description",
        "issue",
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contributor, ContributorAdmin)

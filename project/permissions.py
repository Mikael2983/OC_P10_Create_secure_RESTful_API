from rest_framework import permissions


class IsContributor(permissions.BasePermission):
    """
    Permission pour s'assurer que seul un contributeur peut accéder au projet.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.contributors.all() or request.user == obj.author


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author

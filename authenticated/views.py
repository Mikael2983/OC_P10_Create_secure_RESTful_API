from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, \
    DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from .serializers import UserSerializer, UserListSerializer

User = get_user_model()


class UserCreateView(CreateAPIView):
    """
    View for creating a new user.
    Accessible without authentication.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserListView(ListAPIView):
    """
    View to list users who have authorized the sharing of their data.
    Requires authentication.
    """
    queryset = User.objects.filter(can_data_be_shared=True)
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(RetrieveUpdateAPIView):
    """
    View allowing an authenticated user to view or modify
    only its own information.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        """
        Checks that the user only accesses his own data.
        Raises a PermissionDenied exception if not.
        """
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied(
                "Vous ne pouvez accéder qu'à vos propres informations.")
        return obj


class UserDeleteView(DestroyAPIView):
    """
    View allowing a user to delete their own account.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Check that the user can only delete their own account.
        """
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied(
                "Vous ne pouvez supprimer que votre propre compte.")
        return obj

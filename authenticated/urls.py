from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from authenticated.views import UserCreateView, UserDetailView, UserDeleteView
from django.urls import path


urlpatterns = [
    path('users/register/', UserCreateView.as_view(), name='user-register'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
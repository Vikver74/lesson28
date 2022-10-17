from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserListAPIView, UserDetailAPIView, UserCreateAPIView, UserUpdateAPIView, \
    UserDeleteAPIView


urlpatterns = [
    path('', UserListAPIView.as_view()),
    path('create/', UserCreateAPIView.as_view()),
    path('<int:pk>/', UserDetailAPIView.as_view()),
    path('<int:pk>/update/', UserUpdateAPIView.as_view()),
    path('<int:pk>/delete/', UserDeleteAPIView.as_view()),

    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]

from django.urls import path

from users.views import UserListAPIView, UserDetailAPIView, UserCreateAPIView, LocationViewSet, UserUpdateAPIView, \
    UserDeleteAPIView


urlpatterns = [
    path('', UserListAPIView.as_view()),
    path('create/', UserCreateAPIView.as_view()),
    path('<int:pk>/', UserDetailAPIView.as_view()),
    path('<int:pk>/update/', UserUpdateAPIView.as_view()),
    path('<int:pk>/delete/', UserDeleteAPIView.as_view()),
]

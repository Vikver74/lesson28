from django.urls import path

from users.views import UserListView, UserCreateView, UserDeleteView, UserUpdateView, UserDetailView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list_view'),
    path('create/', UserCreateView.as_view(), name='user_create_view'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete_view'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update_view'),
    path('<int:pk>', UserDetailView.as_view(), name='user_detail_view'),
]
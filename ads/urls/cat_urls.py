from django.urls import path

from ads.views import CategoryCreateAPIView, CategoryUpdateAPIView, CategoryDeleteAPIView, CategoryDetailAPIView, \
    CategoryListAPIView

urlpatterns = [
    path('', CategoryListAPIView.as_view(), name='cat_list_view'),
    path('create/', CategoryCreateAPIView.as_view(), name='cat_create_view'),
    path('<int:pk>/delete/', CategoryDeleteAPIView.as_view(), name='cat_delete_view'),
    path('<int:pk>/update/', CategoryUpdateAPIView.as_view(), name='cat_update_view'),
    path('<int:pk>/', CategoryDetailAPIView.as_view(), name='cat_detail_view'),
]
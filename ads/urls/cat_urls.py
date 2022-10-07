from django.urls import path

from ads.views import CategoryListView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView, CategoryDetailView

urlpatterns = [
    path('', CategoryListView.as_view(), name='cat_list_view'),
    path('create/', CategoryCreateView.as_view(), name='cat_create_view'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='cat_delete_view'),
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='cat_update_view'),
    path('<int:pk>', CategoryDetailView.as_view(), name='cat_detail_view'),
]
from django.urls import path

from ads.views import SelectionAdListView, SelectionAdCreateView, SelectionAdDetailView, SelectionAdDeleteView, \
    SelectionAdUpdateView

urlpatterns = [
    path('', SelectionAdListView.as_view(), name='selection_list_view'),
    path('create/', SelectionAdCreateView.as_view(), name='selection_create_view'),
    path('<int:pk>/', SelectionAdDetailView.as_view(), name='selection_detail_view'),
    path('<int:pk>/delete/', SelectionAdDeleteView.as_view(), name='selection_delete_view'),
    path('<int:pk>/update/', SelectionAdUpdateView.as_view(), name='selection_update_view'),
]

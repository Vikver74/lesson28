from django.urls import path

from ads.views import SelectionAdListView, SelectionAdCreateView, SelectionAdDetailView, SelectionAdDeleteView, \
    SelectionAdUpdateView

urlpatterns = [
    path('', SelectionAdListView.as_view(), name='selection_list_view'),
    path('create/', SelectionAdCreateView.as_view(), name='create_view'),
    path('<int:pk>/', SelectionAdDetailView.as_view(), name='detail_view'),
    path('<int:pk>/delete/', SelectionAdDeleteView.as_view(), name='delete_view'),
    path('<int:pk>/update/', SelectionAdUpdateView.as_view(), name='update_view'),
]

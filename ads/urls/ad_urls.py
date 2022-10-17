from django.urls import path

from ads.views import AdListAPIView, AdUploadImage, AdDetailView, \
    AdCreateAPIView, AdUpdateAPIView, AdDeleteAPIView

urlpatterns = [
    path('', AdListAPIView.as_view(), name='ads_list_view'),
    path('create/', AdCreateAPIView.as_view(), name='ads_create_view'),
    path('<int:pk>/delete/', AdDeleteAPIView.as_view(), name='ads_delete_view'),
    path('<int:pk>/update/', AdUpdateAPIView.as_view(), name='ads_update_view'),
    path('<int:pk>/upload_image/', AdUploadImage.as_view(), name='ads_upload_image'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail_view'),
]

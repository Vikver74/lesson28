from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Category, SelectionAd
from ads.permissions import IsOwnerOrDeny, IsOwnerOrAdminOrModerator
from ads.serializers import AdListSerializer, SelectionAdListSerializer, SelectionAdCreateSerializer, \
    SelectionAdDetailSerializer, SelectionAdDeleteSerializer, SelectionAdUpdateSerializer, AdCreateSerializer, \
    AdUpdateSerializer, AdDeleteSerializer, CategoryCreateSerializer, CategoryUpdateSerializer, \
    CategoryDeleteSerializer, CategoryListSerializer, CategoryDetailSerializer


def index(request):
    return JsonResponse(
        {
            "status": "ok"
        }, safe=False
    )


class AdListAPIView(generics.ListAPIView):
    serializer_class = AdListSerializer
    queryset = Ad.objects.all().order_by('-price')

    def get(self, request, *args, **kwargs):
        category = request.GET.getlist('cat')
        if category:
            self.queryset = self.queryset.filter(category__in=category)
        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location', [])
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().get(self, *args, **kwargs)


class AdDetailView(generics.RetrieveAPIView):
    serializer_class = AdListSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated]


class AdCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdCreateSerializer
    queryset = Ad.objects.all()


class AdUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrModerator]
    serializer_class = AdUpdateSerializer
    queryset = Ad.objects.all()


class AdDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrModerator]
    serializer_class = AdDeleteSerializer
    queryset = Ad.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImage(UpdateView):
    model = Ad
    fields = ['image']
    success_url = '/'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        obj = self.get_object()
        obj.image = request.FILES.get('image')
        obj.save()

        return JsonResponse({
            "id": obj.id,
            "name": obj.name,
            "author_id": obj.author.id,
            "author": obj.author.first_name,
            "price": obj.price,
            "description": obj.description,
            "is_published": obj.is_published,
            "image": obj.image.url,
            "category_id": obj.category.id,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()


class CategoryUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CategoryUpdateSerializer
    queryset = Category.objects.all()


class CategoryCreateAPIView(generics.CreateAPIView):
    serializer_class = CategoryCreateSerializer
    queryset = Category.objects.all()


class CategoryDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CategoryDeleteSerializer
    queryset = Category.objects.all()


class SelectionAdListView(generics.ListAPIView):
    queryset = SelectionAd.objects.all()
    serializer_class = SelectionAdListSerializer


class SelectionAdCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SelectionAd.objects.all()
    serializer_class = SelectionAdCreateSerializer


class SelectionAdUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]
    queryset = SelectionAd.objects.all()
    serializer_class = SelectionAdUpdateSerializer


class SelectionAdDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrDeny]
    queryset = SelectionAd.objects.all()
    serializer_class = SelectionAdDeleteSerializer


class SelectionAdDetailView(generics.RetrieveAPIView):
    queryset = SelectionAd.objects.all()
    serializer_class = SelectionAdDetailSerializer

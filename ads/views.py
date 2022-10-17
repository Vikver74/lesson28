from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import json

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, Category, SelectionAd
from ads.permissions import IsOwnerOrDeny, IsOwnerOrAdminOrModerator
from ads.serializers import AdListSerializer, SelectionAdListSerializer, SelectionAdCreateSerializer, \
    SelectionAdDetailSerializer, SelectionAdDeleteSerializer, SelectionAdUpdateSerializer, AdCreateSerializer, \
    AdUpdateSerializer, AdDeleteSerializer


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


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')
        result = []
        for item in self.object_list:
            result.append({
                "id": item.id,
                "name": item.name
            })

        return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        category = Category.objects.create(name=data['name'])

        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        }, status=201, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
        }, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=204, safe=False)


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

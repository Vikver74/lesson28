from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import json

from ads.models import Ad, Category
from avito import settings
from users.models import User


def index(request):
    return JsonResponse(
        {
            "status": "ok"
        }, safe=False
    )


class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        page_number = request.GET.get('page', 1)
        self.object_list = self.object_list.select_related('author').select_related('category').order_by('-price')
        paginator = Paginator(object_list=self.object_list, per_page=settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page_number)
        result = []
        for item in page_obj:
            result.append({
                "id": item.id,
                "name": item.name,
                "author_id": item.author.id,
                "author": item.author.first_name,
                "price": item.price,
                "description": item.description,
                "is_published": item.is_published,
                "category_id": item.category.id,
                "image": item.image.url,
            })
        return JsonResponse({"items": result, "total": self.object_list.count(), "num_pages": page_obj.number}, safe=False, json_dumps_params={'ensure_ascii': False})


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author.id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "image": self.object.image.url
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        author = get_object_or_404(User, pk=int(data['author']))
        category = get_object_or_404(Category, pk=int(data['category']))
        ad = Ad.objects.create(
            name=data['name'],
            author=author,
            price=data['price'],
            description=data['description'],
            is_published=data['is_published'],
            category=category
        )
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author.id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category.id,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'category']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        author = get_object_or_404(User, pk=int(data['author']))
        category = get_object_or_404(Category, pk=int(data['category']))
        super().post(request, *args, **kwargs)
        if data.get('name'):
            self.object.name = data['name']
        if author:
            self.object.author = author
        if data.get('price'):
            self.object.price = data['price']
        if data.get('description'):
            self.object.description = data['description']
        if category:
            self.object.category = category
        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author.id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


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


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


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

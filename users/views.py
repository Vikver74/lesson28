import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from avito import settings
from users.models import User, Location


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        page_number = request.GET.get('page', 1)
        self.object_list = self.object_list.prefetch_related('location').order_by('username')
        paginator = Paginator(object_list=self.object_list, per_page=settings.TOTAL_ON_PAGE)
        page_obj = paginator.get_page(page_number)
        result = []
        for item in page_obj:
            result.append({
                "id": item.id,
                "username": item.username,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "role": item.role,
                "age": item.age,
                "location": list(map(str, item.location.all())),
                "total_ads": item.ads.count()
            })

        return JsonResponse({"items": result, "total": self.object_list.count(), "num_pages": page_obj.number}, safe=False, json_dumps_params={'ensure_ascii': False})


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            password=data['password'],
            role=data['role'],
            age=data['age']
        )
        for loc in data['location']:
            location, _ = Location.objects.get_or_create(name=loc)
            user.location.add(location)
        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "location": [u.name for u in user.location.all()],
            "age": user.age,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        super().post(request, *args, **kwargs)

        if data.get('first_name'):
            self.object.first_name = data['first_name']
        if data.get('last_name'):
            self.object.last_name = data['last_name']
        if data.get('username'):
            self.object.username = data['username']
        if data.get('password'):
            self.object.password = data['password']
        if data.get('role'):
            self.object.role = data['role']
        if data.get('age'):
            self.object.age = data['age']

        for loc in data['location']:
            location, _ = Location.objects.get_or_create(name=loc)
            self.object.location.add(location)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "location": [u.name for u in self.object.location.all()],
            "age": self.object.age,
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


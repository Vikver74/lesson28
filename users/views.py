from users.models import User, Location

from rest_framework import generics, viewsets

from users.serializers import UserSerializer, UserCreateSerializer, LocationSerializer, \
    UserUpdateSerializer, UserDeleteSerializer, JwtTokenSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class UserDeleteAPIView(generics.DestroyAPIView):
    serializer_class = UserDeleteSerializer
    queryset = User.objects.all()


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class JwtTokenCreateView(generics.CreateAPIView):
    serializer_class = JwtTokenSerializer
    queryset = User.objects.all()

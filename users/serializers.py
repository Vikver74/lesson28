from rest_framework import serializers

from users.models import User, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserCreateSerializer(serializers.ModelSerializer):

    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self.location_ = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for loc in self.location_:
            location_, _ = Location.objects.get_or_create(name=loc.get('name'), lat=loc.get('lat'), lng=loc.get('lng'))
            # location_, _ = Location.objects.get_or_create(name=loc)
            user.location.add(location_)

        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self.location_ = self.initial_data.pop('location')
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)

        for loc in self.location_:
            location_, _ = Location.objects.get_or_create(name=loc.get('name'), lat=loc.get('lat'), lng=loc.get('lng'))
            user.location.add(location_)
        user.save()
        return user


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

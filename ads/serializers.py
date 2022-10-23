from django.core.exceptions import ValidationError
from rest_framework import serializers

from ads.models import Ad, SelectionAd, Category


def validate_is_published(value):
    if value:
        raise ValidationError('is_published must be False')

    return value


class AdListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[validate_is_published])

    class Meta:
        model = Ad
        fields = "__all__"


class AdUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = "__all__"


class AdDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = "__all__"


class SelectionAdListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelectionAd
        fields = ['id', 'name']


class SelectionAdCreateSerializer(serializers.ModelSerializer):
    # items = AdListSerializer(many=True)
    items = serializers.SlugRelatedField(
        slug_field='id',
        many=True,
        queryset=Ad.objects.all()
    )

    class Meta:
        model = SelectionAd
        fields = "__all__"


class SelectionAdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectionAd
        fields = "__all__"


class SelectionAdDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectionAd
        fields = "__all__"


class SelectionAdDetailSerializer(serializers.ModelSerializer):
    items = AdListSerializer(many=True)

    class Meta:
        model = SelectionAd
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

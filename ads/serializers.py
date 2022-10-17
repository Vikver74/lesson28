from rest_framework import serializers

from ads.models import Ad, SelectionAd


class AdListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializer(serializers.ModelSerializer):

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

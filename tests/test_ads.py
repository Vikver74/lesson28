import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_ad(user, api_client, category):
    url = reverse('ads_create_view')
    data = {
        "name": "Новое объявление",
        "author": user.id,
        "price": 100,
        "description": "Описание нового объявления",
        "category": category.id,
        "is_published": False
    }
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['name'] == data['name']
    assert response.json()['author'] == data['author']
    assert response.json()['price'] == data['price']
    assert response.json()['description'] == data['description']
    assert response.json()['category'] == data['category']
    assert response.json()['is_published'] == data['is_published']


@pytest.mark.django_db
def test_list_ad(api_client, ad):
    url = reverse('ads_list_view')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_detail_ad(api_client, ad):
    url = reverse('ad_detail_view', kwargs={'pk': ad.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == ad.id
    assert response.json()['name'] == ad.name
    assert response.json()['category'] == ad.category_id


@pytest.mark.django_db
def test_create_selection_ad(user, api_client, ad):
    url = reverse('selection_create_view')
    data = {
        "name": "Test selection",
        "owner": user.id,
        "items": [ad.id],
    }
    response = api_client.post(url, data=json.dumps(data), content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['name'] == data['name']
    assert response.json()['owner'] == data['owner']
    assert response.json()['items'] == data['items']

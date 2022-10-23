import factory

from users.models import User


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'ads.Category'

    name = 'Локомотивы'
    slug = 'lomotivs'


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'users.User'

    first_name = 'Test'
    last_name = 'Last_test'
    username = 'admin'
    password = '12345'
    role = 'admin'
    birth_date = '2002-01-01'
    email = 'test@test.com'


class AdFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'ads.Ad'

    name = 'Тестовое объявление'
    author = factory.SubFactory(UserFactory)
    price = 100
    description = 'Описание тестового объявления'
    is_published = False
    category = factory.SubFactory(CategoryFactory)


# class SelectionAdFactory(factory.django.DjangoModelFactory):
#
#     class Meta:
#         model = 'ads.SelectionAd'
#
#     name = "Новая подборка"
#     owner = factory.SubFactory(User)
#     items = factory.SubFactory(AdFactory)

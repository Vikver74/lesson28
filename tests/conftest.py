from pytest_factoryboy import register

from tests.factories import AdFactory, UserFactory, CategoryFactory

register(AdFactory)
register(UserFactory)
register(CategoryFactory)

pytest_plugins = "tests.fixtures"

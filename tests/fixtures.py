import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


@pytest.fixture
def api_client(user):
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    return client



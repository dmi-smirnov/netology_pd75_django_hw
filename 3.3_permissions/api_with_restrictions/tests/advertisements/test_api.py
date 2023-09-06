from django.conf import settings
import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from advertisements.models import Advertisement, AdvertisementStatusChoices, UserFavoriteAdvertisement


@pytest.fixture(scope='module')
def user_factory():
    def return_function(**kwargs):
        return baker.make(settings.AUTH_USER_MODEL, **kwargs)
    return return_function

@pytest.fixture(scope='module')
def advertisement_factory():
    def return_function(**kwargs):
        return baker.make(Advertisement, **kwargs)
    return return_function

@pytest.fixture(scope='module')
def api_base_route():
    return '/api/'

@pytest.fixture(scope='module')
def advertisements_route(api_base_route):
    return f'{api_base_route}advertisements/'

@pytest.fixture(scope='module')
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_get_draft_advertisements(user_factory, advertisement_factory,
                                  advertisements_route, api_client):
    # Arrange
    user1, user2 = user_factory(_quantity=2)
    user1_token = Token.objects.create(user=user1).key
    user2_token = Token.objects.create(user=user2).key

    user1_draft_adv = advertisement_factory(creator=user1,
                           status=AdvertisementStatusChoices.DRAFT)
    user2_draft_adv = advertisement_factory(creator=user2,
                           status=AdvertisementStatusChoices.DRAFT)
    
    # Act
    user1_resp = api_client.get(
        path=advertisements_route,
        HTTP_AUTHORIZATION=f'Token {user1_token}'
    )

    user2_resp = api_client.get(
        path=advertisements_route,
        HTTP_AUTHORIZATION=f'Token {user2_token}'
    )

    anon_resp = api_client.get(advertisements_route)

    # Assert
    assert user1_resp.status_code == status.HTTP_200_OK
    user1_resp_data = user1_resp.data
    assert len(user1_resp_data) == 1
    assert user1_resp_data[0]['id'] == user1_draft_adv.id

    assert user2_resp.status_code == status.HTTP_200_OK
    user2_resp_data = user2_resp.data
    assert len(user2_resp_data) == 1
    assert user2_resp_data[0]['id'] == user2_draft_adv.id

    assert anon_resp.status_code == status.HTTP_200_OK
    anon_resp_data = anon_resp.data
    assert len(anon_resp_data) == 0

@pytest.mark.django_db
def test_filter_advertisements_by_favorited(user_factory,
                                            advertisement_factory, advertisements_route,
                                            api_client):
    # Arrange
    user1, user2 = user_factory(_quantity=2)
    user2_token = Token.objects.create(user=user2).key
    
    user1_adv1, user1_adv2 = advertisement_factory(_quantity=2, creator=user1)

    adv_for_user2_favorited = user1_adv1
    UserFavoriteAdvertisement.objects.create(
        user=user2,
        advertisement=adv_for_user2_favorited
    )
    user2_favorite_adv = adv_for_user2_favorited

    # Act
    anon_resp = api_client.get(
        path=advertisements_route,
        data={
            'favorited': True
        }
    )
    user2_resp = api_client.get(
        path=advertisements_route,
        data={'favorited': True},
        HTTP_AUTHORIZATION=f'Token {user2_token}'
    )

    # Assert
    assert anon_resp.status_code == status.HTTP_200_OK
    assert len(anon_resp.data) == 2

    assert user2_resp.status_code == status.HTTP_200_OK
    user2_resp_data = user2_resp.data
    assert len(user2_resp_data) == 1
    assert user2_resp_data[0]['id'] == user2_favorite_adv.id
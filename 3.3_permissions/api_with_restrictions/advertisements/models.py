from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = 'DRAFT', 'Черновик'


class Advertisement(models.Model):
    """Объявление."""
    
    USER_OPEN_ADS_MAX = 10

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    users_favorited = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserFavoriteAdvertisement',
        related_name='favorite_advertisements'
    )


class UserFavoriteAdvertisement(models.Model):
    '''Объявление в избранном пользователя'''

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE
    )

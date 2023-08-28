from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    status = filters.TypedChoiceFilter(
        choices=AdvertisementStatusChoices.choices)

    favorited = filters.BooleanFilter(field_name='favorited',
                                      method='filter_favorited')

    def filter_favorited(self, queryset, name, value):
        if IsAuthenticated().has_permission(self.request, view=None):
            return queryset.filter(users_favorited__in=[self.request.user])
        return queryset

    class Meta:
        model = Advertisement
        fields = ['created_at', 'updated_at', 'status']
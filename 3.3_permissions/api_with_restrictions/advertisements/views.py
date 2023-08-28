from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices, UserFavoriteAdvertisement
from advertisements.permissions import IsOwnerOrAccessToDraftRestricted, IsOwnerOrUpdateAndDeleteRestricted
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrUpdateAndDeleteRestricted,
        IsOwnerOrAccessToDraftRestricted
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def list(self, request, *args, **kwargs):
        '''Модифицированный метод list(), который исключает
        из queryset все объявления-черновики, кроме принадлежащих
        инициатору запроса.'''

        queryset = self.filter_queryset(self.get_queryset())

        # Если инициатор запроса аутентифицирован, то
        if IsAuthenticated().has_permission(self.request, view=None):
            # Исключаем из queryset чужие объявления-черновики
            queryset = queryset.exclude(
                ~Q(creator=self.request.user),
                status=AdvertisementStatusChoices.DRAFT
            )
        # Если инициатор не аутентифицирован, то 
        else:
            # Исключаем из queryset все объявления-черновики
            queryset = queryset.exclude(
                status=AdvertisementStatusChoices.DRAFT
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated,
                                IsOwnerOrAccessToDraftRestricted])
    def favorite(self, request: Request, **kwargs):
        '''Метод для добавления/удаления объявления из избранного
        инициатора запроса'''

        advertisement = self.get_object()

        if request.method == 'POST':
            # Проверяем не является ли инициатор запроса автором
            # добавляемого в избранное объявления
            if request.user == advertisement.creator:
                raise ValidationError(
                    'Advertisement creator cannot add it in favorites.')
            
            # Проверяем имеется ли уже у инициатора запроса
            # добавляемое объявление в избранном
            if UserFavoriteAdvertisement.objects\
                                        .filter(user=request.user)\
                                        .filter(advertisement=advertisement)\
                                        .count():
                raise ValidationError('This advertisement is already in favorites.')

            # Добавляем объявление в избранное инициатора запроса
            UserFavoriteAdvertisement.objects.create(
                user=request.user,
                advertisement=advertisement
            )

            return Response(status=status.HTTP_201_CREATED)
        
        if request.method == 'DELETE':
            user_favorite_advertisment = UserFavoriteAdvertisement.objects.filter(
                user = request.user,
                advertisement = advertisement
            )
            if user_favorite_advertisment:
                user_favorite_advertisment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)

    

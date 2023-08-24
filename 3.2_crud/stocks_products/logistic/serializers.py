from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        copy_validated_data = validated_data.copy()
        # получаем связанные данные для других таблиц
        positions_validated_data = copy_validated_data.pop('positions')
        # получаем данные для склада
        stock_validated_data = copy_validated_data

        # создаем склад по его параметрам
        stock = super().create(stock_validated_data)

        # заполняем связанные таблицы
        for position_validated_data in positions_validated_data:
            StockProduct.objects.create(**position_validated_data,
                                        stock=stock)

        return stock

    def update(self, instance, validated_data):
        copy_validated_data = validated_data.copy()
        # получаем связанные данные для других таблиц
        positions_validated_data = copy_validated_data.pop('positions')
        # получаем данные для склада
        stock_validated_data = copy_validated_data

        # обновляем склад по его параметрам
        stock = super().update(instance, stock_validated_data)

        # обновляем связанные таблицы
        StockProduct.objects.all().filter(stock=stock).delete()
        for position_validated_data in positions_validated_data:
            StockProduct.objects.create(**position_validated_data,
                                        stock=stock)

        return stock
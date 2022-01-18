from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    description = serializers.CharField(min_length=20)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']




class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
        pass


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    #products = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']


    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.create(
                stock=stock,
                product=position.get('product'),
                quantity=position.get('quantity'),
                price=position.get('price')
            )

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,

                product=position.get('product'),

                defaults={
                    'quantity':
                        position.get('quantity'),
                    'price':
                        position.get('price')
                }
            )

        return stock

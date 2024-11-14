from rest_framework import serializers
from items.models import Products
from orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=False)

    class Meta:
        model = Order
        fields = ['id', 'product_id', 'quantity', 'total_price']
        read_only_fields = ['total_price']

    def create(self, validated_data):
        product_id = validated_data.get('product_id', None)
        quantity = validated_data.get('quantity', 0)

        if product_id is not None and quantity > 0:
            try:
                product = Products.objects.get(id=product_id)
            except Products.DoesNotExist:
                raise serializers.ValidationError('Product does not exist')

            total_price = product.price * quantity
            validated_data['total_price'] = total_price
            return super().create(validated_data)

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity', instance.quantity)
        if quantity != instance.quantity:
            try:
                product = Products.objects.get(id=instance.product_id)
            except Products.DoesNotExist:
                raise serializers.ValidationError('Product does not exist')

            total_price = product.price * quantity
            validated_data['total_price'] = total_price
            instance.total_price = total_price
            instance.quantity = quantity
            instance.save()

        return instance





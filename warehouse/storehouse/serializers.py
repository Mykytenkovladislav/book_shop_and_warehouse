from rest_framework import serializers

from .models import Book, BookInstance, Order, OrderItem


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ('id', 'book', 'order_item', 'status',)


class BookSerializer(serializers.HyperlinkedModelSerializer):
    books = BookInstanceSerializer(source="bookinstance_set", many=True)

    class Meta:
        many = True
        model = Book
        fields = (
            'id', 'title', 'author',
            'summary', 'isbn', 'language', 'genre',
            'price', 'books')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'book', 'quantity',)


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source="orderitem_set", many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer_mail', 'order_date', 'shipped_date', 'status', 'order_items',)

    def create(self, validated_data):
        order_items_validated_data = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        order_items_serializer = self.fields['order_items']
        for each in order_items_validated_data:
            each['order'] = order
        order_items = order_items_serializer.create(order_items_validated_data)
        return order

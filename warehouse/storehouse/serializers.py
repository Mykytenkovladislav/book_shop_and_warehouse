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


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    order_items = OrderItemSerializer(source="orderitem_set", many=True)

    class Meta:
        model = Order
        fields = ('id', 'shop_order_id', 'customer_mail', 'order_date', 'shipped_date', 'status', 'order_items',)

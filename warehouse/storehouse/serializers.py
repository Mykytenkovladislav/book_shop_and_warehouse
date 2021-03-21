from rest_framework.views import APIView
from rest_framework import serializers

from .models import Book, BookInstance, Order, OrderItem


class BookInstanceSerializer(serializers.ModelSerializer, APIView):
    class Meta:
        model = BookInstance
        fields = ('id', 'book', 'order_item', 'status',)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'shop_order_id', 'customer_mail', 'order_date', 'shipped_date', 'status',)


class BookSerializer(serializers.ModelSerializer):
    book_instance = BookInstanceSerializer(read_only=True, many=True)

    class Meta:
        many = True
        model = Book
        fields = (
            'id', 'title', 'author',
            'summary', 'isbn', 'language', 'genre',
            'price', 'book_instance')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'book', 'order_item', 'quantity',)

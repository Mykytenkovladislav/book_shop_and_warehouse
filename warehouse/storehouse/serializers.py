from rest_framework.views import APIView
from rest_framework import serializers

from .models import Book, BookInstance, Order, OrderItem


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ('id', 'book', 'order_item', 'status',)


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'shop_order_id', 'customer_mail', 'order_date', 'shipped_date', 'status',)


class BookSerializer(serializers.HyperlinkedModelSerializer):
    books = BookInstanceSerializer(source="bookinstance_set", many=True)

    # TODO Узнать у Ярика как выводить bookintances соеденённые с Book
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
        fields = ('id', 'order', 'book', 'order_item', 'quantity',)

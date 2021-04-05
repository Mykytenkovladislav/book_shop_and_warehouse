from rest_framework import viewsets

from .models import Book, BookInstance, Order, OrderItem, Genre
from .serializers import BookSerializer, BookInstanceSerializer, OrderSerializer, OrderItemSerializer, GenreSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('order')
    serializer_class = OrderItemSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer


class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all().order_by('book__title')
    serializer_class = BookInstanceSerializer


class GenreViewSet(viewsets.ModelViewSet):
    '''ViewSet display all genres'''
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer

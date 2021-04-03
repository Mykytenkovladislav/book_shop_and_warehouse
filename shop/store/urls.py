from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from store.views import BookListView, BookDetailView, contact_form_ajax, add_to_order, order_item_update, \
    order_items_list, order_items_delete, order_send, OrderViewSet

router = routers.DefaultRouter()

router.register(r'orders_api', OrderViewSet)

urlpatterns = [
    url(r'api', include(router.urls)),
    path('', BookListView.as_view(), name='index'),

    path('contact_ajax/', contact_form_ajax, name='contact-ajax'),
    path('<uuid:pk>', BookDetailView.as_view(), name='book-detail'),
    path('add_to_order/<uuid:pk>', add_to_order, name='add_to_order'),
    path('order/', order_items_list, name='order'),
    path('order/send/', order_send, name='order_send'),
    path('order/<int:pk>/update/', order_item_update, name='order_update'),
    path('order/<int:pk>/delete/', order_items_delete, name='order_item_delete'),

]

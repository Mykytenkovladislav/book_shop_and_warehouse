from django.urls import path

from store.views import BookListView, BookDetailView, contact_form_ajax, add_to_order

urlpatterns = [
    path('', BookListView.as_view(), name='index'),

    path('contact_ajax/', contact_form_ajax, name='contact-ajax'),
    path('<uuid:pk>', BookDetailView.as_view(), name='book-detail'),
    path('add_to_order/<uuid:pk>', add_to_order, name='add_to_order'),
]

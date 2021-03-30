from django.urls import path

from store.views import BookListView, BookDetailView, contact_form_ajax

urlpatterns = [
    path('', BookListView.as_view(), name='index'),

    path('contact_ajax/', contact_form_ajax, name='contact-ajax'),
    path('<uuid:pk>', BookDetailView.as_view(), name='book-detail')
]

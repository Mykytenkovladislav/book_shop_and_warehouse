from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('contact_ajax/', views.contact_form_ajax, name='contact-ajax'),
]

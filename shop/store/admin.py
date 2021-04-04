from django import forms
from django.contrib import admin

from .models import Book, Order, OrderItem, Genre


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    order_items = forms.ModelMultipleChoiceField(queryset=OrderItem.objects.all())


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    """Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    list_display = ['title', 'author', 'display_genre']


class OrderItemInlineModelAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', "user", 'order_date', 'shipped_date', 'status', 'comment']
    inlines = [OrderItemInlineModelAdmin]


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']

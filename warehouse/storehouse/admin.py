from django import forms
from django.contrib import admin

from .models import Book, BookInstance, Order, OrderItem


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    order_items = forms.ModelMultipleChoiceField(queryset=OrderItem.objects.all())


class BooksInstanceInlineModelAdmin(admin.StackedInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    """Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - adds inline addition of book instances in book view (inlines)
    """
    list_display = ['title', 'author', 'genre']
    inlines = [BooksInstanceInlineModelAdmin]


@admin.register(BookInstance)
class BookInstanceModelAdmin(admin.ModelAdmin):
    """Administration object for BookInstance models.
    Defines:
     - fields to be displayed in list view (list_display)
     - filters that will be displayed in sidebar (list_filter)
     - grouping of fields into sections (fieldsets)
    """
    list_display = ["id", "book", "status", 'order_item']
    list_filter = ["status", "order_item"]


class OrderItemInlineModelAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['shop_order_id', 'customer_mail', 'order_date', 'shipped_date', 'status']
    inlines = [OrderItemInlineModelAdmin]


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']
    inlines = [BooksInstanceInlineModelAdmin]

from django.contrib import admin

from .models import Book, BookInstance, Order, OrderItems


class BookInlineModelAdmin(admin.TabularInline):
    model = Book


class BooksInstanceInlineModelAdmin(admin.TabularInline):
    """Defines format of inline book instance insertion (used in BookAdmin)"""
    model = BookInstance


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
    list_display = ["id", "book", "status", 'order']
    list_filter = ["status", "order"]
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        # ('Availability', {
        #     'fields': ('status', 'due_back', 'borrower')
        # }),
    )


class OrderItemsInlineModelAdmin(admin.TabularInline):
    model = OrderItems


class OrderInlineModelAdmin(admin.TabularInline):
    model = Order


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['shop_order_id', 'customer_mail', 'order_date', 'shipped_date', 'status']
    inlines = [OrderInlineModelAdmin]


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity']
    inlines = [OrderItemsInlineModelAdmin]

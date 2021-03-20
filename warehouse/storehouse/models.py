import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(_("title"), max_length=200)
    author = models.CharField(_("author"), max_length=200)
    summary = models.TextField(_("summary"), max_length=1000, help_text=_("Enter a brief description of the book"))
    isbn = models.CharField(_("ISBN"), max_length=13, help_text=_("13 character ISBN number"))
    language = models.CharField(_("language"), max_length=20)
    genre = models.CharField(_('genre'), max_length=200)
    price = models.CharField(_('price'), max_length=20, help_text='Book price')

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Order(models.Model):
    """Model representing a customer order (but not a order items)."""

    class OrderStatus(models.IntegerChoices):
        WAITING = 1, _('Waiting')
        IN_PROGRESS = 2, _('In progress')
        DONE = 3, _('Done')

    shop_order_id = models.IntegerField(_('shop order id'), help_text='Shop order id')
    customer_mail = models.EmailField(_('customer mail'), help_text='Customer e-mail address')
    order_date = models.CharField(_('order date'), max_length=20)
    shipped_date = models.DateField(_('order date'), help_text='Date when order moved to Done status')
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.WAITING, blank=True, help_text=_('Order status')
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.shop_order_id


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    class SellStatus(models.IntegerChoices):
        IN_STOCK = 1, _('In stock')
        RESERVED = 2, _('Reserved')
        SOLD = 3, _('Sold')

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, help_text=_("Unique ID for this particular book across whole library")
    )
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=SellStatus.choices, default=SellStatus.IN_STOCK, blank=True, help_text=_('Book status')
    )

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.book.title})"


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(_('quantity'), help_text='Books quantity')

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.order.shop_order_id})"

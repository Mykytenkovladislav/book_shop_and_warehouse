import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE

User = get_user_model()


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, help_text=_("Unique ID for this particular book across whole library")
    )
    title = models.CharField(_("title"), max_length=200)
    author = models.CharField(_("author"), max_length=200)
    summary = models.TextField(_("summary"), max_length=1000, help_text=_("Enter a brief description of the book"))
    isbn = models.CharField(_("ISBN"), max_length=13, help_text=_("13 character ISBN number"))
    language = models.CharField(_("language"), max_length=20)
    genre = models.CharField(_('genre'), max_length=200)
    price = models.FloatField(_('price'), max_length=20, help_text='Book price')

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Order(LifecycleModelMixin, models.Model):
    """Model representing a customer order (but not a order items)."""

    class OrderStatus(models.IntegerChoices):
        WAITING = 1, _('Waiting')
        IN_PROGRESS = 2, _('In progress')
        DONE = 3, _('Done')
        REJECTED = 4, _('Rejected')

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, help_text=_("Unique ID for this order across whole library")
    )
    shop_order_id = models.IntegerField(_('shop order id'), help_text='Shop order id')
    customer_mail = models.EmailField(_('customer mail'), help_text='Customer e-mail address')
    order_date = models.DateField(_('order date'), help_text='Date when order was created')
    shipped_date = models.DateField(_('shipped date'), help_text='Date when order moved to Done status')
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.WAITING, help_text=_('Order status')
    )
    comment = models.CharField(_('order date'), max_length=20, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.shop_order_id}'

    @hook(AFTER_UPDATE, when='status', changes_to=3)
    def order_status_done_email(self):
        send_mail(
            subject="Your order was Done",
            message="Your order was Done",
            from_email="admin@admin.com",  # This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
            recipient_list=[f'{self.customer_mail}', ],  # This is a list
            fail_silently=False  # Set this to False so that you will be noticed in any exception raised
        )

    @hook(AFTER_UPDATE, when='status', changes_to=4)
    def order_status_rejected_email(self):
        from django.core.mail import send_mail

        send_mail(
            subject="Your order was rejected",
            message="Your order was rejected",
            from_email="admin@admin.com",  # This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
            recipient_list=[f'{self.customer_mail}'],  # This is a list
            fail_silently=False  # Set this to False so that you will be noticed in any exception raised
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(_('quantity'), help_text='Books quantity')

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.order.shop_order_id})"


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    class SellStatus(models.IntegerChoices):
        IN_STOCK = 1, _('In stock')
        RESERVED = 2, _('Reserved')
        SOLD = 3, _('Sold')

    id = models.UUIDField(  # noqa: A003
        primary_key=True, default=uuid.uuid4, help_text=_("Unique ID for this particular book across whole library")
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='in_order_item')
    status = models.PositiveSmallIntegerField(
        choices=SellStatus.choices, default=SellStatus.IN_STOCK, blank=True, help_text=_('Book status')
    )

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id} ({self.book.title})"

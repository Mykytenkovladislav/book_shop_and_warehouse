import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


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

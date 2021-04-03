import requests  # noqa
from celery import shared_task

from store.models import Book


@shared_task
def add(x, y):
    print("Here!")
    return x + y


@shared_task
def book_sync():
    url = 'http://127.0.0.1:8002/books'
    response = requests.get(url=url).json()

    for counter, book in enumerate(response):
        if Book.objects.filter(id=book['id']).exists():
            continue
        else:
            Book.objects.create(
                id=book['id'],
                title=book['title'],
                author=book['summary'],
                isbn=book['isbn'],
                language=book['language'],
                genre=book['genre'],
                price=book['price'],
            )
    print('Sync is done')

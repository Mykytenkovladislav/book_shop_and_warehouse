import requests  # noqa
from celery import shared_task

from store.models import Book, Genre


# @shared_task
# def book_sync():
#     url = 'http://warehouse:8002/books'
#     response = requests.get(url=url).json()
#
#     for counter, book in enumerate(response):
#         if Book.objects.filter(id=book['id']).exists():
#             continue
#         else:
#             Book.objects.create(
#                 id=book['id'],
#                 title=book['title'],
#                 author=book['author'],
#                 summary=book['summary'],
#                 isbn=book['isbn'],
#                 language=book['language'],
#                 genre=book['genre'],
#                 price=book['price'],
#             )
#     print('Sync is done')


@shared_task
def book_sync():
    url = 'http://warehouse:8002/books'
    response = requests.get(url=url).json()

    for counter, book in enumerate(response):
        if Book.objects.filter(id=book['id']).exists():
            continue
        else:
            genre_list = []

            for genre_resp in book['genre']:
                genre, created = Genre.objects.get_or_create(name=genre_resp['name'])
                genre_list.append([genre])

            book = Book(
                id=book['id'],
                title=book['title'],
                author=book['author'],
                summary=book['summary'],
                isbn=book['isbn'],
                language=book['language'],
                price=book['price'],
            )
            book.save()
            for genre in genre_list:
                book.genre.add(genre)
                book.save()

    print('Sync is done')

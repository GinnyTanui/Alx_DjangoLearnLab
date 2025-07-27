# Delete Book

## Command:

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
```

## Output:

```python
(1, {'books.Book': 1})
<QuerySet []>
```

✅ Successfully deleted the book. No books remain in the database.

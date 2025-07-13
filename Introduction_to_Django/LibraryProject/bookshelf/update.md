# Update Book

## Command:

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
```

## Output:

```python
'Nineteen Eighty-Four'
```

✅ Successfully updated the book title.

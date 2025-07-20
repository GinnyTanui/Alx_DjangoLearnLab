# Retrieve Book

## Command:

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
```
## Output: 
```python
('1984', 'George Orwell', 1949)
```
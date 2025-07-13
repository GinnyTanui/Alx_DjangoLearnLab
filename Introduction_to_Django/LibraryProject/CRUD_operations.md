# CRUD Operations for Book Model

This document demonstrates the full Create, Retrieve, Update, and Delete operations performed on the `Book` model using the Django shell.

---

## 🟩 Create Book

### Command:

```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
```

### Output:

```python
<Book: 1984>
```

✅ Successfully created the book instance and saved it to the database.

---

## 🔍 Retrieve Book

### Command:

```python
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
```

### Output:

```python
('1984', 'George Orwell', 1949)
```

✅ Successfully retrieved and displayed all attributes of the book.

---

## ✏️ Update Book

### Command:

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book.title
```

### Output:

```python
'Nineteen Eighty-Four'
```

✅ Successfully updated the book title.

---

## ❌ Delete Book

### Command:

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
```

### Output:

```python
(1, {'bookshelf.Book': 1})
<QuerySet []>
```

✅ Successfully deleted the book. No books remain in the database.

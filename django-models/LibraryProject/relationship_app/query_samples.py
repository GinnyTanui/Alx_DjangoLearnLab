import os 
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup() 

from relationship_app.models import Author, Book, Library, Librarian 

#Query 1 
author_name = 'Harry Potter'
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"\Books by {author_name}")
    for book in books_by_author:
         print(f"- {book.title}") 
except Author.DoesNotExist:
     print(f"Books with {author_name} does not exists")
    
#query 2
library_name = "Hometown Library"
try:
     library = Library.objects.get(library_name)
     books_in_library = library.books.all()
     print(f"\nBooks in {library_name}:")
     for book in books_in_library:
        print(f"- {book.title}")
except Library.DoesNotExist:
    print(f"No library found with the name {library_name}") 

try:
    librarian = Librarian.objects.get(name=library_name)
    print(f"\nLibrarian for {library_name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian found for the library {library_name}")
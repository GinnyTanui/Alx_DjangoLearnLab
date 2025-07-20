from django.db import models

# Create your models here. 
class Author(models.Model):
    author = models.CharField(max_length=100) 

class Book(models.Model):
    title = models.CharField(max_length=100) 
    author = models.ForeignKey(Author, on_delete=models.CASCADE) 

class Library(models.Model):
    title = models.CharField(max_length=100)
    books = models.ManyToManyField(Book) 

class Librarian(models.Model):
    title = models.CharField(max_length = 100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)


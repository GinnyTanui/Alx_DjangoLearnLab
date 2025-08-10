from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title 
## the author and boook models created
## the author is a foreign key to the books model 
## author can have mulitple books but a book can only have one author
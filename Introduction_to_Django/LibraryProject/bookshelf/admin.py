from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Show these columns in list view
    list_filter = ('publication_year', 'author')            # Filter by author or year
    search_fields = ('title', 'author')                     # Search bar for title and author


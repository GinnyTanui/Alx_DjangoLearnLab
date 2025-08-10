from rest_framework import serializers 
from .models import Book, Author 

class BookSerializer(serializers.ModelSerializer): 

    publication_year = serializers.SerializerMethodField()
    class Meta:
        model = Book 
        fields = '__all__' 

class AuthorSerializer(serializers.ModelSerializer): 
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = '__all__' 

def get_publication_year(self, obj):
    return obj.publication_year < 2025
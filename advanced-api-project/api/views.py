from django.shortcuts import render
from .models import Author, Book  
from rest_framework import viewsets, generics 
from .serializers import BookSerializer, AuthorSerializer 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError,  PermissionDenied
from datetime import datetime 
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters

# Create your views here.
class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author'] 
    ordering_fields = ['title', 'author', 'publication_year']

class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create books

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")

        publication_year = serializer.validated_data.get("publication_year")
        if publication_year and publication_year > datetime.now().year:
            raise ValidationError({"publication_year": "Publication year cannot be in the future."})
        
        title = serializer.validated_data.get("title")
        if title:
            serializer.validated_data['title'] = title.strip()  # Remove leading/trailing spaces
        serializer.save()

class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update books  

    def perform_update(self, serializer):
       if "author" in serializer.validated_data:
           raise ValidationError("You cannot change the author of a book.") 
       
       publication_year = serializer.validated_data.get("publication_year")
       if publication_year and publication_year > datetime.now().year:
           raise ValidationError({"publication_year": "Publication year cannot be in the future."})

       serializer.save()

class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete books
from django.shortcuts import render
from .models import Author, Book  
from rest_framework import viewsets, generics,filters
from .serializers import BookSerializer, AuthorSerializer 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError,  PermissionDenied
from datetime import datetime 
from rest_framework import generics, filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters



class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(lookup_expr='icontains')
    publication_year = filters.NumberFilter(field_name='publication_date__year')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year'] 

class ListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]

    # Filtering fields
    filterset_class = [BookFilter]

    # Searching fields
    search_fields = ['title', 'author__name']  # assuming author has a name field

    # Ordering fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering
class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow any user to access this view

class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]  # Only authenticated users can create books

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
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]  # Only authenticated users can update books  

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
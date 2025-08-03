from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Book 
from .serializers import BookSerializer 
from rest_framework.permissions import IsAuthenticated, AllowAny , IsAdminUser
from .permissions import IsOwnerorReadOnly 
from rest_framework.authentication import TokenAuthentication
class BookList(generics.ListAPIView): 
    permission_classes = [AllowAny]
    queryset = Book.objects.all() 
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerorReadOnly]  # ✅ Only logged-in owners can edit/delete
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
          serializer.save(owner=self.request.user) 

class AdminBookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]  # ✅ Only admins can access
    queryset = Book.objects.all()
    serializer_class = BookSerializer

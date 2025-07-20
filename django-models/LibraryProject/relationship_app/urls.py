from django.urls import path
from .views import list_books,LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView
urlpatterns = [
    path('book/', list_books, name="list_books"),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
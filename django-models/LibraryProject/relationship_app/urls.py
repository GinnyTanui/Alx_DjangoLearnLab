from django.urls import path
from .views import list_books,LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView
from .import views
urlpatterns = [
    path('book/', list_books, name="list_books"),
    path('register/', views.register.as_view(), name='register'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
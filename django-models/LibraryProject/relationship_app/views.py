from django.shortcuts import render, redirect
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout 
from django.contrib.auth.decorators import login_required
# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books}) 

class LibraryDetailView(DetailView):
    model = Library,
    template_name = "relationship_app/library_detail.html", 
    context_object_name = "library" 

#Registering 
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('logout') #uses authentication form to check user and password, if its correct, gets the user and logs them in automatically
    else:
        form = AuthenticationForm()

    return render(request, 'relationship_app/login.html', {'form': form}) 

def logout_view(request):
    logout(request) 
    return render(request, 'relationship_app/logout.html')
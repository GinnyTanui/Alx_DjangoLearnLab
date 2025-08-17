from django.shortcuts import render
from .forms import UserRegistrationForm, UserProfileForm
from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

       
##profile 
@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserProfileForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        u_form = UserProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': u_form})

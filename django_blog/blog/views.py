from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Register view (handles user registration)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('profile')  # Redirect to the profile page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile view (allows users to view and edit their profile)
@login_required
def profile(request):
    if request.method == 'POST':
        # Allow the user to update their profile info (email, etc.)
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving changes
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})

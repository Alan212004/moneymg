# user/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import Profile

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set password manually
            user.save()

            # Save the Profile with shop_name and phone
            Profile.objects.create(
                user=user,
                shop_name=form.cleaned_data['shop_name'],  # Retrieve from the form
                phone=form.cleaned_data['phone']           # Retrieve from the form
            )
            
            login(request, user)  # Automatically log in the user
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username_or_phone = request.POST.get('username')  # Input field for either username or phone
        password = request.POST.get('password')
        
        # Try to find the user by username first, if not found, try by phone
        try:
            user = User.objects.get(username=username_or_phone)
        except User.DoesNotExist:
            # If no user with that username exists, check phone number
            try:
                user = User.objects.get(profile__phone=username_or_phone)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            # If a user is found, check the password
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard after successful login
            else:
                error_message = "Invalid password"
        else:
            error_message = "Invalid username or phone number"
        
        return render(request, 'user/login.html', {'error': error_message})
    
    return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    return render(request, 'user/profile.html')
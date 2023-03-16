from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View

from .forms import CustomUserCreationForm, ProfileForm


class LoginUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        
        context = {}
        return render(request, 'profiles/login_form.html', context)

    def post(self, request):
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist!')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User loged in successfully')
            return redirect('index')
        
        else:
            messages.error(request, 'Username or Password is incorrect!')

        return redirect('login')


class LogoutUser(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'User was logged out!')
        return redirect('index')


class RegisterUser(View):
    def get(self, request):
        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, 'profiles/register.html', context=context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created successfully')

            login(request, user)

            return redirect('edit-profile')

        else:
            messages.error(request, 'An error occurred during registration')
            return redirect('register')


class EditProfile(View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        context = {'form': form}
        return render(request, 'profiles/profile_form.html', context=context)

    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('index')
        
        else:
            messages.error(request, 'An error occurred during editing profile')


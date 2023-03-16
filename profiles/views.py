from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View

from .forms import CustomUserCreationForm, ProfileForm


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
        

from django.shortcuts import render, redirect
from django.views import View
from .forms import CustomUserCreationForm
from django.contrib import messages

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

        else:
            messages.error(request, 'An error occurred during registration')

        return redirect('index')
    

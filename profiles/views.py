from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View

from .forms import ArtistForm, CustomUserCreationForm, MessageForm, ProfileForm


class LoginUser(View):
    def get(self, request):
        global next_path
        next_path = request.GET.get('next')

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
            # if user wants to submit a review and hasn't loged in, first log in and then redirect to song page
            return redirect(next_path if next_path else 'index')

        else:
            messages.error(request, 'Username or Password is incorrect!')
            return redirect('login')


class LogoutUser(LoginRequiredMixin, View):
    login_url = 'login'

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

            return redirect('edit_profile')

        else:
            messages.error(request, 'An error occurred during registration')
            context = {'form': form}
            return render(request, 'profiles/register.html', context=context)


class EditProfile(LoginRequiredMixin, View):
    login_url = 'login'

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

            is_artist = form.cleaned_data['is_artist']
            if is_artist:
                return redirect('edit_artist')

            return redirect('index')

        else:
            messages.error(request, 'An error occurred during editing profile')
            context = {'form': form}
            return render(request, 'profiles/profile_form.html', context=context)


class EditArtist(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        artist = request.user.profile.artist
        form = ArtistForm(instance=artist)
        context = {'form': form}
        return render(request, 'profiles/artist_form.html', context=context)

    def post(self, request):
        artist = request.user.profile.artist
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artist object updated successfully')
            return redirect('index')
        else:
            messages.error(request, 'An error occurred during editing artist')
            context = {'form': form}
            return render(request, 'profiles/artist_form.html', context=context)


class Contact(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = MessageForm()
        context = {'form': form}
        return render(request, 'profiles/contact_form.html', context=context)

    def post(self, request):
        try:
            sender = request.user.profile
        except:
            sender = None

        form = MessageForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.sender = sender
            form.save()

            messages.success(request, 'Message sent successfully!')
            return redirect('index')

        else:
            messages.error(request, 'An error occurred during sending message')
            context = {'form': form}
            return render(request, 'profiles/contact_form.html', context=context)

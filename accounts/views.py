import html
import html.parser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http.response import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.

form_authentication = AuthenticationForm()
form_creation = UserCreationForm()

def validate_empty_fields(request):
    if not request.POST['username'] or not request.POST['password1'] or not request.POST['password2']:
        return False
    return True


def password_match_validator(request):
    return request.POST['password1'] == request.POST['password2']


def register(request):

    if request.method == 'GET':
        return render(request, 'accounts/register.html', {
            'form': form_authentication
        })

    if not validate_empty_fields(request):
        
        return render(request, 'accounts/register.html', {
            'form': form_authentication,
            'error': 'You need to complete all the fields'

        })

    if password_match_validator(request):
        try:
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password1'])
            login(request, user)
            return redirect('posts:posts')

        except IntegrityError:
            return render(request, 'accounts/register.html', {
                'form': form_creation,
                'error': 'User already exist'
            })

    return render(request, 'accounts/register.html', {
        'form': form_creation,
        'error': 'Password do not match'
    })


def validate_request(request):
    if not request.POST['username'] or not request.POST['password']:
        return False
    return True


def login_user(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {
            'form': AuthenticationForm
        })

    if not validate_request(request):
        return render(request, 'accounts/login.html', {
            'form': AuthenticationForm,
            'error': 'You need to complete all the fields'
        })

    user = authenticate(request, username=request.POST['username'],
                        password=request.POST['password'])
    if user is None:
        return render(request, 'accounts/login.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
        })

    login(request, user)
    return redirect('posts:posts')



def signout(request):
    logout(request)
    return redirect('home')


def search_people(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('accounts:login')
    people = User.objects.all()
    return render(request, 'accounts/search_people.html', {'people': people})
    





import html
import html.parser
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from . models import Follow
from posts.models import Post

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


@login_required
def search_people(request):
    
    people = User.objects.exclude(id=request.user.id)
    followed_user_ids = request.user.followings.values_list('following_id', flat=True)
    people_to_display = people.exclude(id__in=followed_user_ids)
    return render(request, 'accounts/search_people.html', {'people': people_to_display})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
   
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
 
    return redirect('accounts:search_people')


@login_required
def display_profile(request):
    
    user = request.user
    users_following = user.followings.all().count()
    users_followers = user.followers.all().count()
    posts = Post.objects.filter(user = user)
    number_of_posts = posts.count()
    return render(request, 'accounts/profile.html', {'posts': posts,
                                                     'users_following': users_following,
                                                     'users_followers': users_followers,
                                                     'number_of_posts': number_of_posts})

from django.shortcuts import render, redirect, get_object_or_404
from . models import Post, Like, User
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
from django.db.models import Q
from accounts.models import Profile
# Create your views here.

def posts(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('accounts:login')
    
    followed_users = user.followings.values_list('following', flat = True)
    posts = Post.objects.filter(Q(user__in=followed_users) | Q(user=user)).order_by('-created_at')
    for post in posts:
        post.has_liked = post.likes.filter(user=user).exists()
        post.likes_minus_one = post.likes.count() - 1
    return render(request, 'posts/posts.html', {'posts': posts})

def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:posts')    
      
    return render(request, 'posts/create_post.html', {'form': form})

def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("posts:posts")

    return render(request, 'posts/create_post.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(Post, id = pk)
    
    if request.method == 'POST':
        if request.user != post.user:
            return HttpResponse('Unauthorized', status=401)
        if request.user == post.user:
            post.delete()
            return redirect('posts:posts')
    
    return render(request, 'posts/delete_post.html', {'post': post})



def load_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().select_related('user__profile').values(
        'id', 'text', 'user__username', 'created_at', 'user__profile__image')

    comments_data = []
    for comment in comments:
        profile_image_url = comment['user__profile__image'] if comment['user__profile__image'] else '/media/profile_images/default_user.png'
        comments_data.append({
            'id': comment['id'],
            'text': comment['text'],
            'user__username': comment['user__username'],
            'created_at': comment['created_at'],
            'user__profile__image': profile_image_url,
        })

    return JsonResponse(comments_data, safe=False)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if not Like.objects.filter(user=user, post=post).exists():
        Like.objects.create(user=user, post=post)

    likes_count = post.likes.count()
    return JsonResponse({'liked': True, 'likes': likes_count})


@login_required(login_url='/')
def remove_like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if Like.objects.filter(user=user, post=post).exists():
        Like.objects.filter(user=user, post=post).delete()

    likes_count = post.likes.count()
    return JsonResponse({'liked': False, 'likes': likes_count})



def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'user': comment.user.username,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime("%b %d, %Y"),
                    'profile_pic': comment.user.profile.image.url 
                }   
            })
        if form.errors:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)







        
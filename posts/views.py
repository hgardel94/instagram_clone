from django.shortcuts import render, redirect, get_object_or_404
from . models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
# Create your views here.

def posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/posts.html', {'posts': posts})

def create_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
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
        post.delete()
        return redirect('posts:posts')
    
    return render(request, 'posts/delete_post.html', {'post': post})


@login_required(login_url='/')
def like_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            liked = True
        else:
            liked = False
        post.save()
        likes = post.likes.count()
        return JsonResponse({'liked': liked, 'likes': likes})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='/')
def remove_like_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            liked = True
        post.save()
        likes = post.likes.count()
        return JsonResponse({'liked': liked, 'likes': likes})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
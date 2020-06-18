from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Post, Comment
from .forms import PostForm, SearchForm, CommentForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.image=request.FILES['image']
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.image=request.FILES['image']
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_search(request):
    if request.method=='GET':
        form=SearchForm(request.GET)
        query=request.GET.get('q',None)
        if query:
            results= Post.objects.filter(Q(title__icontains=query)| Q(text__icontains=query))
            return render(request, 'blog/post_search.html', {'results':results})
        else:
            return render(request,'blog/404.html',{})
    else:
        print(form.errors)
        return render(request, 'blog/404.html', {})

def post_delete(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request,pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm()
        return render(request,'blog/add_comment_to_post.html',{'form':form})

def handler404(request):
    return render(request, '404.html', status=404)

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail',pk=post_pk)

def login_view(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(request,username=username, password=password)
    if user is not None:
        login(request,user)
        return redirect('post_list.html')
    else:
        return render(request, 'blog/404.html')

def logout_view(request):
    logout(request)
    return redirect('post_list.html')
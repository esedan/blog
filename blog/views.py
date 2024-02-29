from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from account.models import User

# Create your views here.

def home(request):
    post = Post.objects.all()
    context= {
        'posts' : post,
    }
    

    return render(request, 'blog/index.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def post(request):
    form = PostForm()
    context = {
        'form': form
    }
    if request.method=='POST':
        user = request.user
        try:
            User.objects.get(username=user.username)
        except User.DoesNotExist:
            messages.error(request, 'login before creating a post')
            return redirect('home')
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user=request.user
            new_post.save()
            messages.success(request, 'post uploaded successfully')
            return redirect('home')
    return render(request, 'blog/post.html', context)

@login_required(login_url= 'login')
def editPost(request,ref):
    post = Post.objects.get(id=ref)
    form = PostForm(instance= post)
    if request.method == 'POST':
        form= PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'post updated')
            return redirect('home')
    context= {
        'form':form
    }  
    return render(request, 'blog/edit post.html', context)

@login_required(login_url= 'login')
def delete(request, ref):
    if request.method == 'POST':
        post = Post.objects.filter(id=ref).delete()
        messages.success(request, 'post deleted')
        return redirect('home')
    
    return render(request, 'blog/delete.html')
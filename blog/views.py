from django.shortcuts import redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    return render(request, 'blog/post_list.html', {"posts":posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html',{"post":post})

def post_new(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_edit.html',{'form':form})
    

def user_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user)
        return render(request, 'blog/post_list.html', {"posts":posts})
    else:
        return redirect('/')

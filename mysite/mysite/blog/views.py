from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
from member.models import Member
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
import logging
from django.utils import timezone


def post_list(request) :
    all_posts = Post.objects.all().order_by('-id')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_posts, 5)
    posts = paginator.get_page(page)

    return render(request, 'post_list.html', {"posts" : posts})

def post_write(request) :
    if not request.session.get('user'):
        return redirect('member:login')

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            member = Member.objects.get(userid=user_id)
            post = Post()
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.author = member
            #images = request.FILES["imgfile"]
            if request.FILES.get("imgfile") is not None :
                image = request.FILES.get("imgfile")
                fss = FileSystemStorage()
                file = fss.save(image.name, image)
                post.imgfile = file

            post.save()
            return redirect('blog:list')
    else:
        form = PostForm()
    return render(request, 'post_write.html', {"form" : form})

from django.http import Http404

def post_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except:
        raise Http404('게시글을 찾을 수 없습니다.')
    return render (request, 'post_view.html', {'post' : post})

def post_modify(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post':post}
    return render (request, 'post_modify.html', context)

def post_update(request):
    form = PostForm(request.POST)
    if form.is_valid():
        user_id = request.session.get('user')
        member = Member.objects.get(userid=user_id)
        post = Post()
        post.title = form.cleaned_data['title']
        post.content = form.cleaned_data['content']
        post.id = request.POST["post_id"]
        post.author = member
        post.updated_at = timezone.now()
        if request.FILES.get("imgfile") is not None:
            image = request.FILES.get("imgfile")
            fss = FileSystemStorage()
            file = fss.save(image.name, image)
            post.imgfile = file
            post.save(update_fields=['title', 'content', 'imgfile', 'updated_at'])
        else:
            post.save(update_fields=['title', 'content', 'updated_at'])
        return redirect('blog:view', pk=post.id)
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:list')

from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
from datetime import datetime

# Create your views here.


# index
def index(request):
    posts = Post.objects.all().order_by('-pk')
    today = datetime.now().strftime('%Y-%m-%d')
    select_sorting = request.GET.get('select_sorting')
    posts = sorting(posts, select_sorting)
    new_posts(posts)
    context = {
        'today': today,
        'posts': posts,
        'subject': '모든 글',
        'select_sorting': select_sorting,
    }
    return render(request, 'posts/index.html', context)

# 카테고리 filter
def category(request, subject):
    today = datetime.now().strftime('%Y-%m-%d')
    posts = Post.objects.all().filter(category=subject)
    posts2 = Post.objects.all().filter(notice=True)
    posts = posts.union(posts2).order_by('-pk')
    select_sorting = request.GET.get('select_sorting')
    posts = sorting(posts, select_sorting)

    new_posts(posts)

    context = {
        'today': today,
        'posts': posts,
        'subject': subject,
        'select_sorting': select_sorting,
    }
    return render(request, 'posts/index.html', context)

# 정렬
def sorting(queryset, select_sorting):
    if select_sorting == '최신순':
        return queryset.order_by('-pk')
    elif select_sorting == '오래된순':
        return queryset.order_by('pk')
    else:
        return queryset

# new_posts
def new_posts(posts):
    now = timezone.now()
    for post in posts:
        time_diff = now - post.created_at
        if time_diff < timezone.timedelta(hours=1):
            post.is_new = True
        else:
            post.is_new = False



# create
@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            form.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
        'subject': '글 작성',
    }

    return render(request, 'posts/create.html', context)

# 상세페이지
@login_required
def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment_form = CommentForm()
    comments = post.comment_set.all()
    context = {
        'comments': comments,
        'comment_form': comment_form,
        'post': post,
    }
    return render(request, 'posts/detail.html', context)

# 수정
@login_required
def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', post_pk)
    else:
        form = PostForm(instance=post)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'posts/update.html', context)

# 삭제
@login_required
def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.delete()
    return redirect('posts:index')


@login_required
def comment_create(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect('posts:detail', post_pk)


def comments_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:detail', post_pk)
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Follow


def index(request):
    cache.clear()
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def group_posts(request, slug):
    cache.clear()
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'page': page,
         'paginator': paginator,
         'group': group,
         }
    )


@login_required
def new_post(request):
    cache.clear()
    if not request.method == 'POST':
        form = PostForm(files=request.FILES or None)
        return render(request, 'new.html', {'form': form})
    form = PostForm(request.POST, files=request.FILES or None, )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(
        request,
        'new.html',
        {
            'form': form,
            'is_edit': False,
        }
    )


def profile(request, user_id):
    cache.clear()
    user_id = int(user_id)
    post_author = get_object_or_404(User, id=user_id)
    post_list = post_author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    count_following = Follow.objects.filter(user=post_author).count()
    count_follower = Follow.objects.filter(author=post_author).count()
    if request.user.is_anonymous:
        return render(
            request,
            'profile.html',
            {'page': page,
             'paginator': paginator,
             'following': False,
             'author': post_author,
             'profile': post_author,
             'count_following': count_following,
             'count_follower': count_follower,
             }
        )
    f = Follow.objects.filter(user=request.user)
    following_author = []
    for el in f:
        following_author.append(el.author.id)
    if post_author.id in following_author:
        follow = True
    else:
        follow = False
    return render(
        request,
        'profile.html',
        {'page': page,
         'paginator': paginator,
         'following': follow,
         'author': post_author,
         'profile': post_author,
         'count_following': count_following,
         'count_follower': count_follower,
         }
    )


@login_required
def post_view(request, user_id, post_id):
    cache.clear()
    post = get_object_or_404(Post, author__id=user_id, pk=post_id)
    form = CommentForm()
    comments = post.comments.all()
    author = post.author
    print(author)
    return render(request, 'post.html', {
        'post': post,
        'author': author,
        'form': form,
        'comments': comments,
    })


@login_required
def post_edit(request, user_id, post_id):
    cache.clear()
    post = get_object_or_404(Post, author__id=user_id, pk=post_id)
    if post.author != request.user:
        return redirect('post', user_id=user_id, post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('post', user_id=user_id, post_id=post_id)

    form = PostForm(files=request.FILES or None, instance=post)
    return render(
        request,
        'new.html',
        {
            'form': form,
            'is_edit': True,
            'instance': post,
        }
    )


def page_not_found(request, exception):
    cache.clear()
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    cache.clear()
    return render(request, 'misc/500.html', status=500)


@login_required
def add_comment(request, user_id, post_id):
    cache.clear()
    post = get_object_or_404(Post, author__id=user_id, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post', user_id=post.author.id, post_id=post.id)


@login_required
def follow_index(request):
    cache.clear()
    posts = Post.objects.select_related(
        'author',
    ).filter(author__following__user__id=request.user.id)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'follow.html',
        {
            'page': page,
            'paginator': paginator,
        },
    )


@login_required
def profile_follow(request, user_id):
    cache.clear()
    author = get_object_or_404(User, id=user_id)
    if author.id != request.user.id:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', user_id)


@login_required
def profile_unfollow(request, user_id):
    cache.clear()
    author = get_object_or_404(User, id=user_id)
    follow = Follow.objects.filter(author=author, user=request.user.id)
    if follow.exists():
        follow.delete()
    return redirect('profile', user_id)

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Group
from .models import Post
from .models import User


def authorized_only(func):
    def check_user(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect('/auth/login/')

    return check_user


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page,})


@authorized_only
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page,})


def profile(request, username):
    user = User.objects.get(username=username)
    full_name = f'{user.first_name} {user.last_name}'
    number_of_posts = Post.objects.filter(author_id=user.id).count()
    last_post = Post.objects.filter(author_id=user.id).latest('pub_date')
    last_post_text = last_post.text
    pub_date = last_post.pub_date
    post_list = Post.objects.filter(author_id=user.id).exclude(id=last_post.id)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'profile.html',
                  {'username': username,
                   'full_name': full_name,
                   'number_of_posts': number_of_posts,
                   'last_post_text': last_post_text,
                   'latest_post_id': last_post.id,
                   'pub_date': pub_date,
                   'page': page,
                   })

def post_view(request, username, post_id):
    # тут тело функции
    return render(request, 'post.html', {})


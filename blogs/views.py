from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.detail import DetailView

from blogs.forms import PostForm
from blogs.models import Blog, Post
from blogs.sender import send_letter


def send_letter_to_user(blog, path_to_post):
    users = blog.subscribers.all()
    subject = 'New Post'
    for user in users:
        if user.email:
            context = 'New Post in your list of news. Post available for next link: {}'.format(path_to_post)
            send_letter(subject, context, user.email)


@method_decorator(login_required, name='dispatch')
class UserBlogView(View):
    def get(self, request, id):
        data = {}
        current_user = request.user
        blog_owner = User.objects.filter(id=id).first()
        if not blog_owner:
            return HttpResponse('User with id={} does not exist'.format(id))
        data['owner'] = current_user.id == id
        blog, created = Blog.objects.get_or_create(user_owner_id=id)
        data['is_subscribed'] = current_user in blog.subscribers.all()
        posts = Post.objects.filter(created_by=blog_owner)
        data['posts'] = posts
        return render(request, 'blogs/blog.html', data)

    def post(self, request, id):
        blog, created = Blog.objects.get_or_create(user_owner_id=id)
        is_subscribed = request.user in blog.subscribers.all()
        if not is_subscribed:
            blog.subscribers.add(request.user)
            return HttpResponse('{} Subscribed on {} blog'.format(request.user, id))
        else:
            blog.subscribers.remove(request.user)
            return HttpResponse('{} Unsubscribed on {} blog'.format(request.user, id))


@method_decorator(login_required, name='dispatch')
class PostCreateView(View):
    def get(self, request):
        post_form = PostForm()
        return render(request, 'blogs/create_post.html', {'post_form': post_form})

    def post(self, request):
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.created_by = request.user
            post.save()
            blog = Blog.objects.filter(user_owner=request.user).first()
            path = request.build_absolute_uri('/').strip("/")
            path += '/blogs/post/detail/{}/'.format(post.id)
            # Uncomment the next line for sending mail after creation posts
            # send_letter_to_user(blog, path)
            return HttpResponse('OK! Created post with  id:{}'.format(post.id))
        else:
            return HttpResponse('Error data is not valid!')


@method_decorator(login_required, name='dispatch')
class NewsListView(View):
    def get(self, request):
        data = {}
        current_user = request.user
        all_post = []
        for blog in current_user.subscribed_blogs.all():
            news = list(Post.objects.filter(created_by=blog.user_owner).all())
            all_post += news
        all_post = sorted(all_post, key=lambda x: x.data_created, reverse=True)
        data['posts'] = all_post
        return render(request, 'blogs/list_of_news.html', data)


class PostDetailView(DetailView):
    model = Post


def mark_about_read(request, id):
    if request.method == 'GET':
        post = Post.objects.filter(id=id).first()
        if request.user in post.users_by_read.all():
            post.users_by_read.remove(request.user)
            return HttpResponse('{} mark this post as not read'.format(request.user))
        else:
            post.users_by_read.add(request.user)
            return HttpResponse('{} mark this post as already read'.format(request.user))

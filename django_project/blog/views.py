from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Friend, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from .decorators import unauthenticated_user, genuser_only, allowed_users

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListViewVolunteer(ListView):
    model = Post
    template_name = 'blog/home_volunteer.html'   #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    

    def get(self, request):
        posts = Post.objects.all().order_by('-date_posted')
            
        if 'search' in request.GET:
            search_term =  request.GET['search']
            posts = posts.filter(Q(title__icontains = search_term) | 
                                 Q(content__icontains = search_term))

        paginator = Paginator(posts, 5) # Show 5 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        friend, created = Friend.objects.get_or_create(current_user=request.user)
        friends = friend.users.all()
        search_term = ''
                                 
        return render(request, self.template_name, { 'page_obj': page_obj, 'friends': friends})

@method_decorator(genuser_only, name='dispatch')
class PostListViewGenUser(ListView):
    model = Post
    template_name = 'blog/home_genuser.html'   #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    
    

    def get(self, request):

        posts = Post.objects.all().order_by('-date_posted')   
        if 'search' in request.GET:
            search_term =  request.GET['search']
            posts = posts.filter(Q(title__icontains = search_term) | 
                                 Q(content__icontains = search_term))

        paginator = Paginator(posts, 5) # Show 5 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        friend, created = Friend.objects.get_or_create(current_user=request.user)
        friends = friend.users.all()
        search_term = ''
                                 
        return render(request, self.template_name, { 'page_obj': page_obj, 'friends': friends})


class UsersDisplayView(ListView):
    template_name = 'blog/users.html'   #<app>/<model>_<viewtype>.html
    
    def get(self, request):
        users = User.objects.exclude(id = request.user.id)
        friend, created = Friend.objects.get_or_create(current_user=request.user)
        friends = friend.users.all()
        search_term = ''

        if 'search' in request.GET:
            search_term =  request.GET['search']
            users = users.filter(Q(username__icontains = search_term) |
                                Q(first_name__icontains = search_term))

            friends = friends.filter(Q(username__icontains = search_term) |
                                Q(first_name__icontains = search_term))
            
        return render(request, self.template_name, { 'users': users.order_by('first_name'), 'friends': friends.order_by('first_name') })

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'   #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['users'] = User.objects.filter(username = self.kwargs.get('username')).first()
        return data


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'image','content']

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/home/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def not_friend(request):
    return render(request, 'blog/not_friend.html', {'title':'Not Friend'})

def logout_home(request):
    return render(request, 'blog/home_logout.html', { 'posts': Post.objects.all().order_by('-date_posted') })

def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    return HttpResponseRedirect(post.get_home_url())

def dislike_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    return HttpResponseRedirect(post.get_home_url())

def liked_posts(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'blog/liked_posts.html', { 'posts': posts })

def report_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.report.add(request.user)
    messages.warning(request, f'You have reported this post for fake content.')
    return HttpResponseRedirect(post.get_home_url())

def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('users-view')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
from typing import Any, Optional
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post
#from django.http import HttpResponse
from django.views.generic import (
    ListView,
    DetailView,CreateView,UpdateView,
    DeleteView)
def home(request):
    context={
        'posts':Post.objects.all()
    }
    #3rd parameter is used to send data to page
    return render(request, "blog/home.html",context)

# def like_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.user in post.likes.all():
#         post.likes.remove(request.user)
#     else:
#         post.likes.add(request.user)
#         post.dislikes.remove(request.user)
#     return

# def dislike_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.user in post.dislikes.all():
#         post.dislikes.remove(request.user)
#     else:
#         post.dislikes.add(request.user)
#         post.likes.remove(request.user)
#     return redirect('post-detail', pk=post.pk)



class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/users_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        user=get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = self.get_object()
    #     context['comments'] = post.comments.all()  # Fetch comments related to the post
    #     return context


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)
    #prevents other users to edit the post
    def test_func(self) -> bool:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self) -> bool:
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def about(request):
    return render(request,'blog/about.html',{'title':'Aut'}) 

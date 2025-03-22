from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Post, Status
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = Status.objects.get(name="published")
        context["title"] = ("Published")
        context["post_list"] = (
            Post.objects
            .filter(status=published)
            .order_by("created_on").reverse()
        )
        return context
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     status_filter = self.request.GET.get("status", "")
        
    #     if status_filter:
    #         status = Status.objects.get(name=status_filter)
    #         context["post_list"] = Post.objects.filter(status=status).order_by("-created_on")
    #     else:
    #         context["post_list"] = Post.objects.all().order_by("-created_on")
        
    #     return context

class DraftPostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft = Status.objects.get(name="draft")
        context["title"] = ("Draft")
        context["post_list"] = (
            Post.objects
            .filter(status=draft)
            .filter(author=self.request.user)
            .order_by("created_on").reverse()
        )
        return context
    
class ArchivedPostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archived = Status.objects.get(name="archived")
        context["title"] = ("Archived")
        context["post_list"] = (
            Post.objects
            .filter(status=archived)
            .filter(author=self.request.user)
            .order_by("created_on").reverse()
        )
        return context

class PostDetailView(UserPassesTestMixin, DetailView):
    template_name = "posts/detail.html"
    model = Post

    def test_func(self):
        post = self.get_object()
        if post.status.name == "published":
            return True
        elif post.status.name == "draft" and post.author == self.request.user:
            return True
        elif post.status.name == "archived" and self.request.user.is_authenticated:
            return True
        else:
            return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = [
        "title", "subtitle", "body", "status"
    ]

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list") # Update this if your ListView isn't mapped to "list"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # success_url = reverse_lazy("list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
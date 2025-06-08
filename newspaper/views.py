from django.shortcuts import render, get_object_or_404
from .models import Category, Post, Tag
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView

# Create your views here.

from newspaper.models import Advertisement, Post

class SidebarMixin:
       def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False, status = "active"
        ).order_by("-published_at")[:5]
        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )

        return context

class HomeView(SidebarMixin,ListView):
    model = Post
    template_name = "newsportal/home.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(
        published_at__isnull =False, status="active"
    ).order_by("published_at")[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )
        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at","-views_count")[:5]

        return context
    
class PostListView(SidebarMixin,ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")
    
class PostDetailView(SidebarMixin,DetailView):
    model = Post
    template_name = "newsportal/detail/detail.html"
    context_object_name = "post"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_post = self.object
        current_post.views_count +=1
        current_post.save()

        context["related_posts"] = Post.objects.filter(
            published_at__isnull=False, status = "active", category=self.object.category
        ).order_by("-published_at", "-views_count")[:2]

        return context
    

class PostByCategoryView(SidebarMixin,ListView):
    model = Post
    template_name = "about_categories/posts_by_category.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs["category_id"])
        return Post.objects.filter(category=self.category, status='active').order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
    
class CategoryListView(ListView):
    model = Category
    template_name = "about_categories/category_list.html"
    context_object_name = "categories"
    ordering = ["name"]

class TagListView(ListView):
    model = Tag
    template_name = "all_tags/tag_list.html"
    context_object_name = "tags"
    ordering = ["name"]

class PostsByTagView(SidebarMixin,ListView):
    model = Post
    template_name = "all_tags/posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, id=self.kwargs["tag_id"])
        return Post.objects.filter(tag=self.tag, status='active').order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context
    

    
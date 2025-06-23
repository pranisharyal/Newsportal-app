from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy

from newspaper.forms import CommentForm, ContactForm, NewsletterForm, PostForm
from .models import Category, Contact, Post, Tag, TeamMember
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import Q


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
    

class PostByCategoryView(SidebarMixin, ListView):
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
    
class CommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST["post"]

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("post-detail", post_id)
        else:
            post = Post.objects.get(pk=post_id)
            popular_posts = Post.objects.filter(
                published_at__isnull=False, status="active"
            ).order_by("-published_at")[:5]
            advertisement = Advertisement.objects.all().order_by("-created_at").first()
            return render(
                request,
                "newsportal/detail/detail.html",
                {
                    "post":post,
                    "form":form,
                    "popular_posts": popular_posts,
                    "advertisement":advertisement,
                }
            )
        

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = (
            Post.objects
            .prefetch_related("tag")
            .select_related("category")
            .order_by("-created_at")  # or "-id" if no created_at field
        )
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post_form.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "dashboard/post_form.html"
    success_url = reverse_lazy("dashboard")

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "dashboard/post_confirm_delete.html"
    success_url = reverse_lazy("dashboard")

class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = "newsportal/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully!"

class AboutPageView(TemplateView):
    template_name = "newsportal/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        return context
    
class NewsletterView(View):
    def post(self, request):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                    "success": True,
                    "message": "Successfully subscribed to the newsletter.",
                    },
                    status =201,
                )
            
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Cannot subscribe to the newsletter.",
                    },
                    status=400,
                )
        
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX XMLHttpRequest",
                },
                status=400,
            )

class PostSearchView(View):
    template_name = "newsportal/list/list.html"

    def get(self, request, *args, **kwargs):
        print(request.GET)
        query = request.GET["query"]
        post_list = Post.objects.filter(
            (Q(title__icontains=query) | Q(content__icontains=query))
            & Q(status="active")
            & Q(published_at__isnull=False)
        ).order_by(
            "-published_at"
        )
        page = request.GET.get("page", 1)
        paginate_by = 1
        paginator = Paginator(post_list, paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)

        popular_posts = Post.objects.filter(
            published_at__isnull=False, status = "active"
        ).order_by("-published_at")[:5]
        advertisement = Advertisement.objects.all().order_by("-created_at").first()

        return render(
            request,
            self.template_name,
            {
                "page_obj": posts,
                "query": query,
                "popular_posts":popular_posts,
                "advertisement":advertisement,
            }
        )

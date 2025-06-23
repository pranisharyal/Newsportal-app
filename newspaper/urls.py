
from django.urls import path
from django.contrib.auth import views as auth_views
from newspaper import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("category/<int:category_id>/", views.PostByCategoryView.as_view(), name="posts_by_category"),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tag/<int:tag_id>/', views.PostsByTagView.as_view(), name='posts_by_tag'),
    path('comment/', views.CommentView.as_view(), name="comment"),
    path("post/create/", views.PostCreateView.as_view(), name="post-create"),
    path("post/update/<int:pk>/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/delete/<int:pk>/", views.PostDeleteView.as_view(), name="post-delete"),
    path("contact/", views.ContactCreateView.as_view(), name="contact"),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path("newsletter/", views.NewsletterView.as_view(), name="newsletter"),
    path("search/", views.PostSearchView.as_view(), name="search"),
]

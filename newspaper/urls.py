
from django.urls import path

from newspaper import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path("post-list/", views.PostListView.as_view(), name="post-list"),
    path("post-detail/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("category/<int:category_id>/", views.PostByCategoryView.as_view(), name="posts_by_category"),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tag/<int:tag_id>/', views.PostsByTagView.as_view(), name='posts_by_tag'),
]

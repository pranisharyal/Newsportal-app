from rest_framework import exceptions
from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone


from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from api.serializers import CategorySerializer, ContactSerializer, GroupSerializer, NewsletterSerializer, PostPublishSerializer, PostSerializer, TagSerializer, UserSerializer
from newspaper.models import Category, Contact, Newsletter, Post, Tag
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tags to be viewed or edited.
    """
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Categoryss to be viewed or edited.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ["list", "retrieve"]:
            queryset = queryset.filter(status="active", published_at__isnull=False)

        return queryset
        
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return super().get_permissions()
    
class PostListByCategoryView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permissions_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status="active",
            published_at__isnull=False,
            category=self.kwargs["category_id"],
        )
        return queryset
    
class PostListByTagView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            status="active",
            published_at__isnull = False,
            tag=self.kwargs["tag_id"],
        )
        return queryset
    
class DraftListView(ListAPIView):
    queryset = Post.objects.filter(published_at__isnull=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

class DraftDetailView(RetrieveAPIView):
    queryset = Post.objects.filter(published_at__isnull=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]

class PostPublishViewSet(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = PostPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data

            post = Post.objects.get(pk=data["id"])
            post.published_at = timezone.now()
            post.save()
            serialized_data = PostSerializer(post).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        
class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ["list", 'retrieve', "destroy"]:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)
    
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ["list", "retrieve", "destroy"]:
                 return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    def update(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(request.method)
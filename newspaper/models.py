from django.db import models

# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"] #Categories.object.all ma alphabet order ma basxa
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Tag(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ('in_active', 'Inactive'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y,%m/%d", blank=False) #imagefield ko lagi pillow install garnu parxa
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    views_count = models.PositiveBigIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
class Advertisement(TimeStampModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="advertisements/%Y/%m/%d", blank=False)

    def __str__(self):
        return self.title
    
class UserProfile(TimeStampModel):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_images/%Y/%m/%d", blank=False)
    address = models.CharField(max_length=200)
    biography = models.TextField()

    def __str__(self):
        return self.user.username
    
class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    content = models.TextField()
    def __str__(self):
        return f"{self.content[:50]} | {self.user.username}"
    
class Contact(TimeStampModel):
    message = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["created_at"]

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    about = models.TextField()
    image = models.ImageField(upload_to='team_images/')

    def __str__(self):
        return self.name
    
class Newsletter(TimeStampModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
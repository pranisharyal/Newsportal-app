from django import forms
from newspaper.models import Comment, Contact, Newsletter, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["post", "content"]
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'featured_image', 'status', 'category', 'tag', 'published_at']
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields ="__all__"


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = "__all__"
        

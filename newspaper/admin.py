from django.contrib import admin

from newspaper.models import Advertisement, Category, Comment, Contact, Post, Tag, TeamMember, UserProfile
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Advertisement)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(TeamMember)



class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)
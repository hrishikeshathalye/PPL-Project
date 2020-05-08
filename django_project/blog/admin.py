from django.contrib import admin
from .models import Post, Friend, Comment

admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(Comment)
from django.contrib import admin
from .models import Post, Friend, Comment

admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(Comment)
admin.site.site_header = 'Covid Connect Admin'
admin.site.site_title = 'Covid Connect Admin'
admin.site.index_title = 'Welcome to the Covid Connect Admin Area!'
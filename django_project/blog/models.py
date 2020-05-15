from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(default='default.jpg', upload_to='post_pics')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank = True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank = True)
    report = models.ManyToManyField(User, related_name='report', blank = True) 

    def __str__(self):
        return self.title

    def get_absolute_url(self):
            return reverse('post-detail', kwargs={'pk':self.pk})    

    def get_home_url(self):
        return reverse('home-genuser')

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        img = img.resize((600,400), Image.ANTIALIAS)
        output_size = (img.width,img.height )
        img.thumbnail(output_size)
        img.save(self.image.path)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
        

class Friend(models.Model):
        users = models.ManyToManyField(User)
        current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete = models.CASCADE)

        @classmethod
        def make_friend(cls, current_user, new_friend):
            friend, created = cls.objects.get_or_create(
                current_user=current_user
            )
            friend.users.add(new_friend)

        @classmethod
        def lose_friend(cls, current_user, new_friend):
            friend, created = cls.objects.get_or_create(
                current_user=current_user
            )
            friend.users.remove(new_friend)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
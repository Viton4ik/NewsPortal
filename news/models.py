
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    authorRating = models.SmallIntegerField(default=0)

    # обновляет рейтинг пользователя, переданный в аргумент этого метода. состоит из следующего:
    def update_rating(self):
        # суммарный рейтинг всех комментариев к статьям автора.
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
    #     print(postRat, pRat)
        pRat += postRat.get('postRating')

        # суммарный рейтинг всех комментариев автора;
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
    #     print(commentRat, cRat)
        cRat += commentRat.get('commentRating')

        # суммарный рейтинг каждой статьи автора умножается на 3;
        self.authorRating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'
    # def __str__(self):
    #     return f'{self.authorUser.username}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    news = 'news'
    post = 'post'
    CONTENT_TYPE = [
        (news, 'новость'),
        (post, 'статья'),
    ]
    contentType = models.CharField(max_length=4, choices=CONTENT_TYPE, default=post)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    createTime = models.DateTimeField(auto_now_add=True)
    topic = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.SmallIntegerField(default=0)

    # get editing time
    editTime = models.DateTimeField(null=True)

    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце
    def preview(self):
        return f"{self.content[0:123]}..."

    def __str__(self):
        return f'{self.topic.title()}: {self.content[:20]}... Created: {self.createTime}\n'

    # link to the name 'post_detail' in urls.py if using generics
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    # change the cache if the post has been changed
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)      # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.id}')    # затем удаляем его из кэша, чтобы сбросить его


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.postThrough.content[:64]}...'


class Comment(models.Model):
    text = models.TextField()
    createTime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'

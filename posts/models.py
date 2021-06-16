from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группы',
        help_text='Выберите группу',
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст',
    )
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True, null=True,
        verbose_name='Изображение',
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User, related_name='follower', on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'author'],
            name='following_unique'
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст',
    )
    created = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text

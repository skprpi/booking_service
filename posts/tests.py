from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import TestCase, Client

from posts.models import Post, Group, Follow, Comment

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.username = 'StasBasov'
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()
        cls.group = Group.objects.create(
            title='testGroup',
            slug='tg',
            description='Group for test'
        )
        cls.user2 = User.objects.create_user(username='UserWithoutName')

    def test_homepage(self):
        response = self.unauthorized_client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        """Авторизованный пользователь может опубликовать пост (new)"""
        current_posts_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('new_post'),
            {'text': 'Это текст публикации'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), current_posts_count + 1)

    def test_force_login(self):
        response = self.authorized_client.post(reverse('new_post'))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_newpage(self):
        """Неавторизованный посетитель не может опубликовать пост
        (его редиректит на страницу входа)"""
        response = self.unauthorized_client.get(reverse('new_post'))
        login_url = reverse('login')
        new_post_url = reverse('new_post')
        target_url = f'{login_url}?next={new_post_url}'
        self.assertRedirects(
            response,
            target_url,
            status_code=302,
            target_status_code=200
        )

    def test_publication(self):
        """После публикации поста новая запись появляется на главной
        странице сайта (index), на персональной странице пользователя
        (profile), и на отдельной странице поста (post)"""
        self.authorized_client.post(
            reverse('new_post'),
            {'text': 'Это текст публикации'},
            follow=True,
        )
        post = Post.objects.get(author=self.user)
        reverse_list = self.get_reverse_list(post)
        post_index = post.pk
        for rev in reverse_list:
            response = self.authorized_client.get(rev)
            self.assertContains(response, post_index)

    def test_edit_post(self):
        """Авторизованный пользователь может отредактировать свой пост,
        после этого содержимое поста изменится на всех связанных страницах."""
        self.authorized_client.post(
            reverse('new_post'),
            {'text': 'Это текст публикации', 'group': self.group.id},
            follow=True,
        )
        post = Post.objects.get(author=self.user)
        old_post_text = post.text
        self.authorized_client.post(
            reverse(
                'post_edit', kwargs={
                    'username': self.username,
                    'post_id': post.id
                }
            ),
            {
                'text': 'Это новый текст публикации',
                'group': self.group.id,
                'author': self.user,
                'pk': post.id,
            },
            follow=True
        )
        post_edited = Post.objects.get(pk=1)
        reverse_list = self.get_reverse_list(post)
        for rev in reverse_list:
            response = self.authorized_client.get(rev)
            self.assertContains(response, post_edited.text)
            self.assertNotContains(response, old_post_text)

    def test_img_on_page(self):
        img = self.get_img()
        self.authorized_client.post(
            reverse('new_post'),
            {'text': 'Это текст публикации 1', 'image': img},
            follow=True,
        )
        response = self.authorized_client.get(
            reverse('post', kwargs={'username': self.username, 'post_id': 1})
        )
        self.assertContains(response, '<img')
        self.authorized_client.post(
            reverse('new_post'),
            {'text': 'Это текст публикации 2'},
            follow=True,
        )
        response = self.authorized_client.get(
            reverse('post', kwargs={'username': self.username, 'post_id': 2})
        )
        self.assertNotContains(response, '<img')

    def test_correct_img_on_pages(self):
        img = self.get_img()
        self.authorized_client.post(
            reverse('new_post'),
            {
                'text': 'Какой-то текст',
                'image': img,
                'group': self.group.id,
            },
            follow=True,
        )
        post = Post.objects.get(pk=1)
        reverse_list = self.get_reverse_list(post)
        for rev in reverse_list:
            response = self.authorized_client.get(rev)
            self.assertContains(response, '<img')

    def test_not_img_file(self):
        with open('hello.txt', 'w') as file:
            file.write('Some text')
            file.close()
        with open('hello.txt', 'rb') as file:
            response = self.authorized_client.post(
                reverse('new_post'),
                {'text': 'Тест на картинку',
                 'group': self.group.id,
                 'image': file,
                 },
                follow=True)
            self.assertFormError(response, 'form', 'image',
                                 'Загрузите правильное изображение. '
                                 + 'Файл, который вы загрузили, '
                                 + 'поврежден или не является изображением.')

    def get_reverse_list(self, post):
        return [
            reverse('index', kwargs={}),
            reverse('profile', kwargs={'username': self.username}),
            reverse('post', kwargs={
                'username': self.username, 'post_id': post.id
            })
        ]

    def test_auth_follow(self):
        """Авторизованный пользователь может подписываться
        на других пользователей и удалять их из подписок."""
        authorized_client = Client()
        authorized_client.force_login(self.user)
        authorized_client.get(
            reverse('profile_follow',
                    kwargs={'username': self.user2.username}),
            follow=True,
        )
        authorized_client.force_login(self.user2)
        post_check = authorized_client.post(
            reverse('new_post'),
            {'text': 'Новый пост!'},
            follow=True)
        post_check = Post.objects.first()
        response = self.authorized_client.get(
            reverse('follow_index'),
            follow=True,
        )
        self.assertContains(response, post_check.text)

    def test_auth_unfollow(self):
        follow = Follow.objects.create(author=self.user2, user=self.user)
        post = Post.objects.create(author=self.user2, text='Some text')
        authorized_client = Client()
        authorized_client.force_login(self.user)
        authorized_client.get(
            reverse('profile_unfollow',
                    kwargs={'username': self.user2.username}),
            follow=True,
        )
        response = self.authorized_client.get(
            reverse('follow_index'),
            follow=True,
        )
        self.assertNotContains(response, post.text)

    def test_follow_show(self):
        """Новая запись пользователя появляется в ленте тех,
        кто на него подписан и не появляется в ленте тех
        кто не подписан на него."""
        user2 = User.objects.create_user(username='User2')
        user3 = User.objects.create_user(username='User3')
        post = Post.objects.create(author=self.user, text='Hello world')
        post2 = Post.objects.create(author=user2, text='Hello2')
        post3 = Post.objects.create(author=user3, text='Hello3')
        follow = Follow.objects.create(user=self.user, author=user3)
        response = self.authorized_client.post(
            reverse('follow_index')
        )
        self.assertContains(response, post3.text)
        self.assertNotContains(response, post2.text)
        self.assertNotContains(response, post.text)

    def test_comment_authorized_user(self):
        """Только авторизированный пользователь может комментировать посты."""
        user2 = User.objects.create_user(username='User2')
        post = Post.objects.create(author=user2, text='Пример поста')
        comment = Comment.objects.create(
            author=self.user,
            post=post,
            text='Some text',
        )
        response = self.authorized_client.get(
            reverse('post',
                    kwargs={'username': user2.username, 'post_id': post.id})
        )
        self.assertContains(response, comment.text)
        wrong_response = self.unauthorized_client.get(
            reverse('add_comment',
                    kwargs={'username': user2.username, 'post_id': post.id})
        )
        login_url = reverse('login')
        new_post_url = reverse('add_comment',
                               kwargs={'username': user2.username,
                                       'post_id': post.id})
        target_url = f'{login_url}?next={new_post_url}'
        self.assertRedirects(
            wrong_response,
            target_url,
        )

    def test_comment_unauthorized_user(self):
        """Только авторизированный пользователь может комментировать посты."""
        post = Post.objects.create(author=self.user2, text='Пример поста')
        wrong_response = self.unauthorized_client.get(
            reverse('add_comment',
                    kwargs={'username': self.user2.username,
                            'post_id': post.id})
        )
        login_url = reverse('login')
        new_post_url = reverse('add_comment',
                               kwargs={'username': self.user2.username,
                                       'post_id': post.id})
        target_url = f'{login_url}?next={new_post_url}'
        self.assertRedirects(
            wrong_response,
            target_url,
        )

    def test_cache(self):
        key = make_template_fragment_key('index_page')
        response_old = self.authorized_client.get(reverse('index'))
        new_post = Post.objects.create(author=self.user, text='Пример поста')
        response_new = self.authorized_client.get(reverse('index'))
        cache.touch(key, 0)
        response_newest = self.authorized_client.get(reverse('index'))
        self.assertNotEqual(response_old.content, response_newest.content)

    def get_img(self):
        img_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b')
        img = SimpleUploadedFile(
            'cat.gif',
            img_gif,
            content_type='image/gif'
        )
        return img

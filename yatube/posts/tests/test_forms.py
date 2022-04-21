from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Test_name')
        cls.post = Post.objects.create(
            author=cls.author,
            text='test_post',
        )

    def setUp(self):
        self.user = User.objects.create_user(username='ilmarinen')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post.
        """
        posts = Post.objects.count() + 1
        form = {
            'text': 'test_text_form'
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form,
            follow=True
        )
        self.assertEqual(
            Post.objects.count(),
            posts,
        )
        text_queryset = Post.objects.filter(text='test_text_form')
        text_queryset = str(text_queryset)
        self.assertIn(form['text'], text_queryset)

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post.
        """
        post = Post.objects.count()
        form = {
            'text': 'test_text_form'
        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form,
            follow=True,
        )
        self.assertEqual(
            Post.objects.count(),
            post,
        )
        self.post.refresh_from_db()
        self.assertEqual(
            self.post.text,
            form['text']
        )

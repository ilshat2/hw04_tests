from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from http import HTTPStatus
from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author_client = Client()
        cls.author = User.objects.create_user(
            username='Test_name',
            email='test@gmail.com',
            password='password',)
        cls.author_client.force_login(cls.author)
        cls.group = Group.objects.create(
            title='Ж',
            description='Тестовое описание',
            slug='zh',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовый пост',
            group=cls.group,
        )

    def setUp(self) -> None:
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Vainamoinen')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_url_exists_at_desired_location(self):
        """Домашняя страница / доступна любому пользователю.
        """
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_url_exists_at_desired_location(self):
        """Созданная в setUpClass тестовая группа/страница
        по адресу /group/zh/ доступна любому пользователю.
        """
        response = self.guest_client.get('/group/zh/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_url_exists_at_desired_location(self):
        """Страница /posts/1/ доступна любому пользователю.
        """
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю.
        """
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonynous(self):
        """Страница по адресу /create/ перенаправит анонимного
        пользователя на страницу логина.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_private_url(self):
        """Без авторизации приватные URL недоступны."""
        url_names = (
            '/create/',
            '/admin/',
        )
        for adress in url_names:
            with self.subTest():
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон.
        Авторизованный пользователь.
        """
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/zh/': 'posts/group_list.html',
            '/profile/Vainamoinen/': 'posts/profile.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_unexisting_page_url_exists_at_desired_location(self):
        """Несуществующая страница (ошибка 404)
        доступна любому пользователю.
        """
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

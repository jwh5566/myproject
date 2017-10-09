from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from boards.views import home, board_topics, new_topic
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
from boards.views import new_topic
from boards.forms import NewTopicForm


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        User.objects.create(username='john', email='john@doe.com', password='123')

    def test_new_topic_view_success_status_code(self):
        """
        test new_topic view retun success status code
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        """
        test when board is not in the database
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        """
        test new_topic is mapping new_topic view
        :return:
        """
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        """
        test new topic veiw have link to the board_topic
        :return:
        """
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        """
        test post valid data
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())  # Topic.objects.exists() check table topic is or not null，
                                                 # because test database is null and here is just create a instance
        self.assertTrue(Post.objects.exists())

    def test_new_topic_with_valid_post_data(self):
        """
        invalid data should not redirect
        expected behavior is show form again with validation errors.
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_data_with_empty_fields(self):
        """
        invalid data should not redirect
        expected behavior is show form again with validation errors.
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_contains_form(self):
        """
        test new_topic have a form
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):
        """
        Invalid data should not redirect
        The expected behavior is show the form with the validation error.
        :return:
        """
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)  # check form.errors is not null


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


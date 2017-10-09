from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from boards.views import home, board_topics, new_topic
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
from boards.views import new_topic
from boards.forms import NewTopicForm


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        """
        test home page return code 200
        :return:
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """
        test home url is mapping home view
        :return:
        """
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        """
        test home page have link to the board_topics
        :return:
        """
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))


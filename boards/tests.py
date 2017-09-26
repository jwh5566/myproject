from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from .views import home


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        """
        test home page return code 200
        :return:
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        """
        test home url is mapping home view
        :return:
        """
        view = resolve('/')
        self.assertEqual(view.func, home)
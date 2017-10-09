from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse


from ..models import Board, Post, Topic
from ..views import topic_posts
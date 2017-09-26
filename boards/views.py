from django.shortcuts import render
from django.http import HttpResponse
from .models import Board


def home(request):
    # return HttpResponse('Hello World!')
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


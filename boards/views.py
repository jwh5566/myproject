from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from .forms import NewTopicForm


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    # if request.method == 'POST':
    #     subject = request.POST['subject']
    #     message = request.POST['message']
    #     user = User.objects.first()   # get the current logged user
    #     topic = Topic.objects.create(
    #         subject=subject,
    #         board=board,
    #         starter=user
    #     )
    #     post = Post.objects.create(
    #         message=message,
    #         topic=topic,
    #         created_by=user
    #     )
    #     return redirect('board_topics', pk=board.pk)
    # return render(request, 'new_topic.html', {'board': board})
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', pk=board.pk)
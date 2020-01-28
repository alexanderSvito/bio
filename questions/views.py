import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from questions.models import Question, TestSuite

TEST_LENGTH = 10


@login_required
def start(request):
    suite = TestSuite.objects.create(
        user=request.user
    )
    for question in random.sample(list(Question.objects.all()), TEST_LENGTH):
        suite.questions.add(question)
    suite.save()
    return redirect("/test/1")


@login_required
def question(request, pk=None):
    return render(request, 'test.html', context={
        "pk": pk
    })

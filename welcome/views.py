import datetime

from questions.models import Question
from django.shortcuts import render


def main_view(request):
    if request.method == 'GET':
        return render(
            request,
            "main.html",
            context={
                "now": datetime.datetime.now(),
                "questions": Question.objects.all()
            }
        )


def about_view(request):
    if request.method == 'GET':
        return render(
            request,
            "about.html",
            context={
                "now": datetime.datetime.now()
            }
        )

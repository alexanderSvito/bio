import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import TemplateView, ListView

from questions.models import Question
from django.shortcuts import render, get_object_or_404


def main_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            is_exists = request.user.test_suites.filter(
                is_active=True
            ).exists()
        else:
            is_exists = False
        return render(
            request,
            "main.html",
            context={
                "now": datetime.datetime.now(),
                "questions": Question.objects.all(),
                "is_exists": is_exists
            }
        )


def generic(request, pk=None):
    question = get_object_or_404(Question, pk=pk)
    return HttpResponse("")


class AboutView(TemplateView):
    template_name = 'about.html'


class LearnView(ListView):
    queryset = Question.objects.filter(text__contains='АТФ')


# def about_view(request):
#     return render(
#         request,
#         "about.html",
#     )

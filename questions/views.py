import random

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone

from questions.models import Question, TestSuite, TestAnswer

TEST_LENGTH = 10


@login_required(login_url='/login')
def start(request):
    suite = TestSuite.objects.create(
        user=request.user,
        is_active=True
    )
    for question in random.sample(list(Question.objects.all()), TEST_LENGTH):
        suite.questions.add(question)
    suite.save()
    return redirect("/test/1")


@login_required
def continue_view(request):
    index = request.last_answered
    return redirect(f"/test/{index + 1}")


def questions_view(request):
    questions = Question.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, 5)
    return render(request, 'questions.html', context={
        "questions": paginator.page(page),
        "page": page
    })


@login_required
def question(request, pk=None):
    test_suite = request.user.get_active_test_suite()
    question = test_suite[pk - 1]
    if request.method == 'GET':
        return render(request, 'test.html', context={
            "pk": pk,
            "question": question
        })
    elif request.method == 'POST':
        answer = request.POST.get("answer")
        if answer is None:
            return redirect(f"/test/{pk}")
        answer = question.answers.get(no=answer)
        test_question_answer = TestAnswer.objects.get(
            question=question, testsuite=test_suite
        )
        if answer.is_correct:
            test_question_answer.is_correct = True
            test_suite.correct_count += 1
        else:
            test_question_answer.is_correct = False
        test_question_answer.answered_at = timezone.now()
        test_question_answer.save()
        test_suite.save()

        request.session['last_answered'] = pk

        if pk == 10:
            test_suite.is_active = False
            test_suite.save()
            return render(request, "final.html", context={
                "test_suite": test_suite
            })
        return redirect(f"/test/{pk + 1}")


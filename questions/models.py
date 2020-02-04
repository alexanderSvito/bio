from django.contrib.sessions.models import Session
from django.db import models
from django.contrib.auth import get_user_model


class TestSuite(models.Model):
    session = models.OneToOneField(
        Session,
        related_name='test_suites',
        on_delete=models.CASCADE,
        null=True
    )
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(
        get_user_model(),
        related_name='test_suites',
        on_delete=models.CASCADE
    )
    correct_count = models.PositiveSmallIntegerField(
        default=0
    )

    def __getitem__(self, item):
        return self.questions.all()[item]


class Question(models.Model):
    test_suites = models.ManyToManyField(
        TestSuite,
        related_name='questions',
        through='TestAnswer'
    )
    text = models.TextField()
    is_test = models.BooleanField(default=False)
    explaining = models.TextField()
    image = models.ImageField(upload_to='img', null=True)

    def __str__(self):
        return self.text if len(self.text) < 200 else self.text[:200]


class TestAnswer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    testsuite = models.ForeignKey(
        TestSuite,
        on_delete=models.CASCADE
    )
    no = models.PositiveSmallIntegerField(default=0)
    is_correct = models.NullBooleanField(null=True)
    answered_at = models.DateTimeField(null=True)


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=256)
    no = models.IntegerField()
    is_correct = models.BooleanField(default=False)
    image = models.ImageField(upload_to='img', null=True)






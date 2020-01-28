from django.db import models
from django.contrib.auth import get_user_model


class TestSuite(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='test_suites',
        on_delete=models.CASCADE
    )


class Question(models.Model):
    test_suites = models.ManyToManyField(
        TestSuite,
        related_name='questions',
    )
    text = models.TextField()
    is_test = models.BooleanField(default=False)
    explaining = models.TextField()
    image = models.ImageField(upload_to='img', null=True)

    def __str__(self):
        return self.text


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






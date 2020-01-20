from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=512)

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






from django.contrib import admin
from questions.models import Question, Answer, TestSuite

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(TestSuite)

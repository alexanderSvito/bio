import json
import os

from django.core.management import BaseCommand

from questions.models import Question, Answer
from django.conf import settings


SEED_DATA_DIR = os.path.join(
    settings.BASE_DIR,
    'data',
    'questions'
)


class Command(BaseCommand):
    help = 'Populates database with seed data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--truncate',
            '-t',
            default=False,
            action='store_true'
        )

    def handle(self, *args, **options):
        if options['truncate']:
            Question.objects.all().delete()
            Answer.objects.all().delete()
            self.stdout.write("Truncated DB")

        for filename in os.listdir(SEED_DATA_DIR):
            with open(os.path.join(
                SEED_DATA_DIR,
                filename
            )) as f:
                data = json.load(f)

            if data['attachments']['question']:
                question_image = data['attachments']['question'][0]
            else:
                question_image = None

            if data['is_test']:
                question = Question.objects.create(
                    id=data['#id'],
                    text=data['question'],
                    is_test=data['is_test'],
                    explaining=data['explaining'],
                    image=question_image
                )

                for option_id, option_text in data['options']:
                    if data['attachments']['answer']:
                        answer_image = data['attachments']['answer'][0]
                    else:
                        answer_image = None
                    answer = Answer(
                        no=option_id,
                        text=option_text,
                        image=answer_image,
                        is_correct=data['correct'] == option_id
                    )
                    answer.question = question
                    answer.save()

                self.stdout.write(f"Question #{question.id} created")




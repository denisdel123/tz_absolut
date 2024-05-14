from django.core.management import BaseCommand

from usersApp.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.get(email='denis_belenko@mail.ru')
        answers = users.answer.all()
        for answer in answers:
            print(answer.question.text)
            print(answer.text_answer)
            print(answer.choice_answer)

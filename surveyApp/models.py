from django.db import models

from app import settings

# словарь для определения необязательных полей
NULLABLE = {
    'null': True,
    'blank': True
}

# переменные для выбора типа вопроса
TEXT = 'text'
CHOICE = 'choice'

QUESTION_TYPE = [
    (TEXT, 'text'),
    (CHOICE, 'choice')
]

"""Модель опроса имеет поле всех вопросов question."""


class Survey(models.Model):
    title = models.CharField(max_length=40, verbose_name='Названия опроса')
    description = models.TextField(**NULLABLE, verbose_name='Описание опроса')
    at_start = models.DateTimeField(**NULLABLE, verbose_name='Дата начала опроса')
    at_end = models.DateTimeField(**NULLABLE, verbose_name='Дата завершение опроса')

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __repr__(self):
        return 'Модель опроса'


"""Модель вопросов имеет поле ответов answer."""


class Question(models.Model):
    survey = models.ForeignKey(
        Survey,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name='принадлежность к опросу')

    text = models.TextField(verbose_name='Текст вопроса')

    question_type = models.CharField(
        max_length=15,
        choices=QUESTION_TYPE,
        default=TEXT,
        verbose_name='Тип вопроса')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __repr__(self):
        return "Модель вопроса"


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answer',
        verbose_name='Принадлежность вопросу')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answer',
        verbose_name='Принадлежность к пользователю')

    text_answer = models.TextField(**NULLABLE, verbose_name='Текстовый ответ')
    choice_answer = models.CharField(**NULLABLE, verbose_name='Список ответов')

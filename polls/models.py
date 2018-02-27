from django.db import models
from django.contrib.auth.models import User


class AnswerType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    answer_type = models.ForeignKey(AnswerType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class AnswerChoice(models.Model):
    value = models.CharField(max_length=200)
    answer_type = models.ForeignKey(AnswerType,
                                    on_delete=models.CASCADE,
                                    related_name='choices')

    def __str__(self):
        return self.value


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'choice')

    def __str__(self):
        return self.user.username + " : " + self.question.title + " -> " + self.choice.value

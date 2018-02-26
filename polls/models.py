from django.db import models


class AnswerType(models.Model):
    name = models.CharField(max_length=50)


class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    answer_type = models.ForeignKey(AnswerType, on_delete=models.CASCADE)


class AnswerChoice(models.Model):
    value = models.CharField(max_length=200)
    answer_type = models.ForeignKey(AnswerType, on_delete=models.CASCADE)


class UserAnswer(models.Model):
    ident = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAnswer, on_delete=models.CASCADE)

from django.contrib import admin
from .models import AnswerType, Question, AnswerChoice, Answer

admin.site.register(AnswerType)
admin.site.register(Question)
admin.site.register(AnswerChoice)
admin.site.register(Answer)
# Register your models here.

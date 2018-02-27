from django import forms
from .models import Question, Answer


class LamouliesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LamouliesForm, self).__init__(*args, **kwargs)
        for question in Question.objects.all():
            self.fields['question_%d' % question.pk] = forms.ModelChoiceField(
                label=question.title,
                queryset=question.answer_type.choices,
                to_field_name='value',
                help_text=question.description)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('question', 'choice')

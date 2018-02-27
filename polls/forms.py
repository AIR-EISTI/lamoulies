from django import forms
from .models import Question


class LamouliesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LamouliesForm, self).__init__(*args, **kwargs)
        for question in Question.objects.all():
            self.fields['question[%d]' % question.pk] = forms.ModelChoiceField(
                label=question.title,
                queryset=question.answer_type.choices,
                to_field_name='value')

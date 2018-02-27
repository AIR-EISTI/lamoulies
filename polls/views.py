from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import Question, Answer
from .forms import LamouliesForm
from .utils import getResults


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'error': 'not_authenticated'})

    user = [e for e in request.user
                              .social_auth
                              .filter(provider='google-openidconnect')
            if e.extra_data.get('hd') == 'eisti.eu']

    if not len(user):
        return render(request, 'index.html', {'error': 'domain'})
    form = LamouliesForm(request.POST or None)
    if form.is_valid():
        for question_id, response in form.cleaned_data.items():
            pk = int(question_id.split('_')[1])
            Answer.objects.create(user=request.user,
                                  choice=response,
                                  question=Question.objects.get(pk=pk))

    saved = form.is_valid()
    return render(request, 'index.html', {'form': form, 'saved': saved})


def stats(request):
    if not request.user.is_staff:
        return HttpResponseForbidden

    questions = {question: getResults(question) for question in Question.objects.all()}
    return render(request, 'stats.html', {'questions': questions})

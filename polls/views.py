from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .models import Question
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
    questions = Question.objects.all()
    return render(request, 'index.html', {'questions': questions, 'form': form})


def stats(request):
    if not request.user.is_staff:
        return HttpResponseForbidden

    questions = {question: getResults(question) for question in Question.objects.all()}
    print(questions)
    return render(request, 'stats.html', {'questions': questions})

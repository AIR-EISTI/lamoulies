from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from .models import Question, Answer, AnswerType
from .forms import LamouliesForm, AnswerForm
from .utils import getResults, isUserAuthenticatedAndEistiStudent



def home(request):
    is_auth_eisti, error = isUserAuthenticatedAndEistiStudent(request)
    if not is_auth_eisti:
        return render(request, 'index.html', {'error': error})

    initial = {
        'question_%d' % answer.question.pk: answer.choice
        for answer in request.user.answer_set.all()
        }

    form = LamouliesForm(initial=initial)
    return render(request, 'index.html', {'form': form})


@csrf_exempt
def postAnswer(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    is_auth_eisti, error = isUserAuthenticatedAndEistiStudent(request)
    if not is_auth_eisti:
        return HttpResponseForbidden()
    form = AnswerForm(request.POST)

    if form.is_valid():
        question = form.cleaned_data['question']
        answer = Answer.objects.filter(
            question=question,
            user=request.user)
        if not answer:
            answer = Answer(question=question, user=request.user)
        else:
            answer = answer.first()

        answer.choice = form.cleaned_data['choice']

        answer.save()
        return HttpResponse(status=204)
    return JsonResponse(dict(form.errors.items()), status=400)


@csrf_exempt
def delAnswer(request, pk=None):
    if request.method != 'DELETE':
        return HttpResponse(status=405)

    is_auth_eisti, error = isUserAuthenticatedAndEistiStudent(request)
    if not is_auth_eisti:
        return HttpResponseForbidden()

    try:
        answer = request.user.answer_set.get(question__pk=pk)
        answer.delete()
        return HttpResponse(status=204)
    except Answer.DoesNotExist:
        return HttpResponse(status=404)


@csrf_exempt
@staff_member_required
def getQuestionResults(request, pk=None):
    if request.method != 'GET':
        return HttpResponse(status=405)

    question = get_object_or_404(Question, pk=pk)
    result_list = getResults(question)
    paginator = Paginator(result_list, 5)

    results_page = paginator.get_page(request.GET.get('page'))

    next_page_number = None
    if results_page.has_next():
        next_page_number = results_page.next_page_number()

    data = {'results': results_page.object_list, 'next_page': next_page_number}
    return JsonResponse(data, safe=False)


@staff_member_required
def stats(request):
    return render(request, 'stats.html', {'questions': Question.objects.all()})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

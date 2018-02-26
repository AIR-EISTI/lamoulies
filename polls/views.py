from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'error': 'not_authenticated'})

    user = [e for e in request.user.social_auth.filter(provider='google-oauth2')
            if e.extra_data.get('domain') == 'eisti.eu']

    if not len(user):
        return render(request, 'index.html', {'error': 'domain'})
    return render(request, 'index.html')

# Create your views here.

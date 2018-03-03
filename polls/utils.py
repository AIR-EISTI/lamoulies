from operator import itemgetter
from django.contrib.auth import logout


def getResults(question):
    results = [
                (choice.value, question.answer_set.filter(choice=choice).count())
                for choice in question.answer_type.choices.all()
              ]
    results.sort(key=itemgetter(1), reverse=True)
    return results


def isUserAuthenticatedAndEistiStudent(request):
    if not request.user.is_authenticated:
        return (False, 'not_authenticated')

    user = [e for e in request.user
                              .social_auth
                              .filter(provider='google-openidconnect')
            if e.extra_data.get('hd') == 'eisti.eu']

    if not len(user):
        logout(request)
        return (False, 'domain')
    return (True, None)

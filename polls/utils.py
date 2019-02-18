from operator import itemgetter
from django.contrib.auth import logout
from hashlib import md5


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


def social_pipeline_anonymisation(details, response, *args, **kwargs):
    sub = response['sub']
    details['username'] = md5((details['username'] + sub).encode()).hexdigest()
    details['email'] = md5((details['email'] + sub).encode()).hexdigest()
    return details

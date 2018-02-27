from operator import itemgetter


def getResults(question):
    results = [
                (choice.value, question.answer_set.filter(choice=choice).count())
                for choice in question.answer_type.choices.all()
              ]
    results.sort(key=itemgetter(1), reverse=True)
    return results

from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.views import generic

class IndexView(generic.ListView):
    """To show the index page which show all published question"""
    
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte = timezone.now(),
            choice__isnull = False).distinct().order_by("pub_date")[:5]


class DetailView(generic.DetailView):
    """To show the detail page with question and its choices."""
    model = Question
    template_name = "polls/details.html"

    def get_queryset(self):
        #Excludes any questions that aren't published yet.
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")


class ResultView(generic.DetailView):
    """To show result page which show question and vote for each choice."""    
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """To update the vote of selected choice in database by 1.

    Args:
        request: Http request object
        question_id (_type_): Unique identifier to check against which question choice is selected 

    Returns:
        Http respose: send data to result for specific question.
    """

    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except Choice.DoesNotExist:
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message": "You did not select a choice"
            },
        )
    else:
        #F here is use to access directly value of fields of db 
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args = (question_id,)))



                    #FOR PRACTICE AND EXPLORING DIFFERENT THINGS

# def index(request):
# #    latest_question = Question.objects.all()[:5]
# #    page = loader.get_template("polls/index.html")
# #    context = {
# #        "latest_question_list" : latest_question
# #    }
# #    return HttpResponse(page.render(context,request))
# #can use simple render without loading page in other variable
#     #latest_question = Question.objects.all()[:5]
#     # context = {
#     #     "latest_question_list" : latest_question
#     # }
#     # return render(request, "polls/index.html", context)
#     return render(request, "polls/index.html", {"latest_question_list" : Question.objects.all()[:5]})


# def details(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "polls/details.html", {"question" : get_object_or_404(Question, pk=question_id)})

# def results(request, question_id):
#     return render(request, "polls/result.html", {"question" : get_object_or_404(Question, pk=question_id)})
from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse

class QuestionTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """It should return false 
        If the publication date of the question is in the future
        """
        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_question(self):
        """It should return false 
        If the publication date of the question is in the past
        """
        time = timezone.now() - datetime.timedelta(days = 3)
        past_question = Question(pub_date = time)
        self.assertIs(past_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """It should return true 
        If the publication date of the question is in last 24 hours
        """
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)


    def test_was_published_recently_with_choice(self):
        """It should return false if question have no choice"""

        question = create_question(question_text = 'Past question', days = -1)
        self.assertIs(question.choice_set.exists(), False)


def create_question(question_text, days):
    """Create a question with the given question_text and published the
    given number of days offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    
    Args:
        question_text:  For text of quesition e.g. Your name?
        days: To store publication date of the question
    """
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text, pub_date = time)


def create_question_with_choice(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).

    Args:
        question_text:  For text of quesition e.g. Your name?
        days: To store publication date of the question
    """
    time = timezone.now() + datetime.timedelta(days = days)
    question = Question.objects.create(question_text = question_text, pub_date = time)
    Choice.objects.create(question = question, choice_text = "choice 1")
    return question

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """To check if no question exits, correct message display or not"""

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """To check quesiton with publication date in past will display or not.
        It should display question.
        """

        question = create_question_with_choice(question_text = 'Past question.', days = -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )
    
    def test_future_question(self):
        """To check quesiton with publication date in future will display or not.
        It should not display the question with future date.
        """

        question = create_question(question_text = 'future question', days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

    def test_future_and_past_question(self):
        """To check quesiton with publication date in past and future.
        Only question with publication date in past should display.
        """

        question = create_question_with_choice(question_text = "Past question.", days = -30)
        create_question_with_choice(question_text = "Future question.", days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )
    
    def test_two_past_question(self):
        """To check multiple quesiton with publication date in past will display or not.
        It should display slice of 5 if more than 5 else all.
        """

        question1 = create_question_with_choice(question_text = 'Past question 1', days = -30)
        question2 = create_question_with_choice(question_text = 'Past question 2', days = -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question1, question2],
        )
    

    class QuestionDetailViewTests(TestCase):
        
        def test_future_question(self):
            """To check if try to access question with publication date in future.
            It should display 404 Error
            """
            future_question = create_question_with_choice(question_text = "future quesiton", days = 20)
            response = self.client.get(reverse("polls:detail", args = (future_question.id,)))
            self.assertEqual(response.status_code, 404)

        def test_past_question(self):
            """To check if question with publication date in past show question detail or not.
            It should display question detail.
            """

            past_question = create_question_with_choice(question_text = "past quesiton", days = -20)
            response = self.client.get(reverse("polls:detail", args = (past_question.id,)))
            self.assertContains(response, past_question.question_text)
             
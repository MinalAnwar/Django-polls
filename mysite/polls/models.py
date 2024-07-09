import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    """This model is used to create table in database named quesition
    with two attributes
    Args:
        modles (question_text): For text of quesition e.g. Your name?
        models (pub_date): For saving the date when question was generated.
    """    


    def __str__(self):
        return self.question_text


    def was_published_recently(self):
        """This is used to check that question is generated in 
        last 24 hours or not

        Returns:
            boolean: is question generated in last 24 hours true else false
        """        
        now = timezone.now()
        return now - datetime.timedelta(days = 1) <= self.pub_date <= now

    question_text = models.CharField(max_length = 200)
    #this first arg string make the attribute human readable 
    #give it a name else it remain machine readable 
    pub_date = models.DateTimeField("date publised") 

class Choice(models.Model):
    """This is to store choice against each question using
    ORM foreign key relation

    Args:
        models (question): Store the question against which choice will store.
        models (choice_text): To store the text of choice.
        models (votes): Store number of time choice is selected.
    """    


    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)


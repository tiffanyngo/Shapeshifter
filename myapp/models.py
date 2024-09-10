from django.db import models
from datetime import date
from django.contrib.auth.models import User

class StateAssessment(models.Model):
    OPTIONS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    ]

    choice = models.CharField(
        max_length=10,
        choices=OPTIONS,
        default='6'
    )
    form_submission_date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

class PresenceAssessment(StateAssessment):
    pass

class ThoughtsAssessment(StateAssessment):
    pass

class FeelingsAssessment(StateAssessment):
    pass

class ActionsAssessment(StateAssessment):
    pass

class BehavioursAssessment(StateAssessment):
    pass

class DecisionAssessment(StateAssessment):
    pass

class NaturalnessAssessment(StateAssessment):
    pass

class Intention(models.Model):
    identity = models.CharField(blank=True, max_length = 100, default = '')
    action = models.TextField(blank=True, default = '')
    feeling = models.TextField(blank=True,  default = '')
    form_submission_date = models.DateField(default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1 )  
    def print_info(self):
        print(f'Identity: {self.identity}')
        print(f'Feeling: {self.feeling}')
        print(f'Action: {self.action}')
        print(f'Intention object (Feeling: {self.feeling}, Action: {self.action})')


class Shift(models.Model):
    contradictory_beliefs = models.TextField()
    form_submission_date = models.DateField(default=date.today)
    realigned_beliefs = models.TextField()
    presence_shift = models.TextField()
    decision_techniques = models.TextField()
    promises = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)  


    
class UserSignUp(models.Model):
    username = models.CharField(   
        max_length=150,
        unique=True
        )
    password = models.CharField(
     max_length=128
        )
    email = models.EmailField(
    blank=True
        )


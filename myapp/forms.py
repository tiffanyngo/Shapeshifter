from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import PresenceAssessment, ThoughtsAssessment, FeelingsAssessment, ActionsAssessment, BehavioursAssessment, DecisionAssessment, NaturalnessAssessment, Intention, Shift, UserSignUp
class BaseStateAssessmentForm(forms.ModelForm):
    class Meta:
        fields = ['choice']
        widgets = {
            'choice': forms.RadioSelect
        }

class PresenceAssessmentForm(BaseStateAssessmentForm):
    class Meta(BaseStateAssessmentForm.Meta):
        model = PresenceAssessment

class ThoughtsAssessmentForm(BaseStateAssessmentForm):
    class Meta(BaseStateAssessmentForm.Meta):
        model = ThoughtsAssessment


class FeelingsAssessmentForm(BaseStateAssessmentForm):
    class Meta(BaseStateAssessmentForm.Meta):
        model = FeelingsAssessment

class ActionsAssessmentForm(BaseStateAssessmentForm):
    class Meta(BaseStateAssessmentForm.Meta):
        model = ActionsAssessment

class BehavioursAssessmentForm(BaseStateAssessmentForm):
    class Meta(BaseStateAssessmentForm.Meta):
        model = BehavioursAssessment

class DecisionAssessmentForm(BaseStateAssessmentForm):
    class Meta(BaseStateAssessmentForm.Meta):
        model = DecisionAssessment

class NaturalnessAssessmentForm(BaseStateAssessmentForm):
    class Meta(BaseStateAssessmentForm.Meta):
        model = NaturalnessAssessment


class DateDataSelectionForm(forms.Form):
    date = forms.ChoiceField(choices=[], label='Select a Date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get unique dates that have data submitted (both past and today)
        dates_with_submissions = PresenceAssessment.objects.values_list('form_submission_date', flat=True).distinct()
        
        # Ensure the dates are sorted in descending order
        dates_with_submissions = sorted(dates_with_submissions, reverse=True)
        
        # Prepare choices with existing dates
        choices = [(str(date), str(date)) for date in dates_with_submissions]
        
        # Update the date field's choices
        self.fields['date'].choices = choices
        
class IntentionForm(forms.ModelForm):
    class Meta:
        model = Intention
        fields = ['identity', 'action', 'feeling']
       

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['contradictory_beliefs','realigned_beliefs','presence_shift','decision_techniques', 'promises']
        widgets = {'contradictory_beliefs': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
                   'realigned_beliefs': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
                   'presence_shift': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
                   'decision_techniques': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
                   'promises': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
                   
                   }
        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = UserSignUp
        fields = ['username', 'password', 'email']

class UsernameRetrievalForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user with this email address.")
        return email


        


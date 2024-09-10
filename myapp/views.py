from django.shortcuts import render, redirect
from .forms import (
    PresenceAssessmentForm,
    ThoughtsAssessmentForm,
    DateDataSelectionForm,
    IntentionForm,
    ShiftForm,
    UserSignUpForm,
    UserLoginForm
)
from .models import PresenceAssessment, ThoughtsAssessment, FeelingsAssessment, ActionsAssessment, BehavioursAssessment, DecisionAssessment, NaturalnessAssessment, Intention, Shift
from django.utils import timezone
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import UsernameRetrievalForm
from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings


 
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
 # Ensure this li1ne is included

def some_view(request):
    response = HttpResponse("This is your view response content.")
    response['ngrok-skip-browser-warning'] = 'true'
    return response



@login_required
def home_view(request):
    if request.method == 'POST' and 'submit_decision' in request.POST:
        user_input = request.POST.get('identity','').strip()
        if not user_input:
            return render(request, 'myapp/identity.html')
        else:
            return redirect(f"{reverse('assessment_view')}?user_input={user_input}")
    else:
        return render(request, 'myapp/identity.html')

@login_required
def assessment_view(request):
    user = request.user
    user_input = request.GET.get('user_input', '')
    date_selection_form = DateDataSelectionForm()
    fill_in_the_blanks_intention_form = IntentionForm()
    shift_form = ShiftForm()

    if 'submit_assessment' in request.POST:
        presence_choice = request.POST.get('presence')
        thoughts_choice = request.POST.get('thoughts')
        feelings_choice = request.POST.get('feelings')
        actions_choice = request.POST.get('actions')
        behaviours_choice = request.POST.get('behaviours')
        decision_choice = request.POST.get('decision_assessment')
        naturalness_choice = request.POST.get('naturalness')

        if presence_choice and thoughts_choice and feelings_choice and actions_choice and behaviours_choice and decision_choice and naturalness_choice:
            PresenceAssessment.objects.create(
                choice=presence_choice,
                form_submission_date=timezone.localtime(timezone.now()).date(),
                user=user
            )
            ThoughtsAssessment.objects.create(
                choice=thoughts_choice,
                form_submission_date=timezone.localtime(timezone.now()).date(),
                user=user
            )
            FeelingsAssessment.objects.create(
                choice=feelings_choice,
                form_submission_date=timezone.localtime(timezone.now()).date(),
                user=user
            )
            ActionsAssessment.objects.create(
                choice=actions_choice,
                form_submission_date=timezone.localtime(timezone.now()).date(),
                user=user
            )
            BehavioursAssessment.objects.create(
                choice=behaviours_choice,
                form_submission_date=timezone.localtime(timezone.now()).date(),
                user=user
            )
            DecisionAssessment.objects.create(
                choice=decision_choice,
                form_submission_date=timezone.localtime(timezone.now()).date(),
                user=user
            )
            NaturalnessAssessment.objects.create(
                choice=naturalness_choice,
                form_submission_date=timezone.localtime(timezone.now()).date(),
                user=user
            )

            return redirect('submitted_results')

    elif 'submit_intention' in request.POST:
        fill_in_the_blanks_intention_form = IntentionForm(request.POST)
        shift_form = ShiftForm(request.POST)

        if fill_in_the_blanks_intention_form.is_valid() and shift_form.is_valid():
            fill_in_the_blanks_intention = fill_in_the_blanks_intention_form.save(commit=False)
            fill_in_the_blanks_intention.identity = user_input
            fill_in_the_blanks_intention.user = user
            fill_in_the_blanks_intention.save()

            shift_instance = shift_form.save(commit=False)
            shift_instance.user = user
            shift_instance.form_submission_date = timezone.localtime(timezone.now()).date()
            shift_instance.save()

            return redirect(f"{reverse('submitted_intention')}?user_input={user_input}")

    return render(request, 'myapp/index.html', {
        'date_selection_form': date_selection_form,
        'fill_in_the_blanks_intention': fill_in_the_blanks_intention_form,
        'user_input': user_input,
        'shift_form': shift_form
    })

@login_required
def submitted_assessment(request):
    user = request.user
    today = timezone.localdate()

    presence_assessment_results = PresenceAssessment.objects.filter(user=user, form_submission_date=today)
    thoughts_assessment_results = ThoughtsAssessment.objects.filter(user=user, form_submission_date=today)
    feelings_assessment_results = FeelingsAssessment.objects.filter(user=user, form_submission_date=today)
    actions_assessment_results = ActionsAssessment.objects.filter(user=user, form_submission_date=today)
    behaviours_assessment_results = BehavioursAssessment.objects.filter(user=user, form_submission_date=today)
    decision_assessment_results = DecisionAssessment.objects.filter(user=user, form_submission_date=today)
    naturalness_assessment_results = NaturalnessAssessment.objects.filter(user=user, form_submission_date=today)

    return render(request, 'myapp/submitted_form.html', {
        'presence_assessment_results': presence_assessment_results,
        'thoughts_assessment_results': thoughts_assessment_results,
        'feelings_assessment_results': feelings_assessment_results,
        'actions_assessment_results': actions_assessment_results,
        'behaviours_assessment_results': behaviours_assessment_results,
        'decision_assessment_results': decision_assessment_results,
        'naturalness_assessment_results': naturalness_assessment_results
    })

@login_required
def selected_date_submission_results(request):
    user = request.user
    selected_date = request.GET.get('date')

    if selected_date:
        try:
            selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            presence_data = PresenceAssessment.objects.filter(user=user, form_submission_date=selected_date_obj)
            fill_in_blanks_data = Intention.objects.filter(user=user, form_submission_date=selected_date_obj)
        except ValueError:
            presence_data = None
            fill_in_blanks_data = None
    else:
        presence_data = None
        fill_in_blanks_data = None

    date_selection_form = DateDataSelectionForm()

    return render(request, 'myapp/selected_date_data.html', {
        'presence_data': presence_data,
        'fill_in_blanks_data': fill_in_blanks_data,
        'selected_date': selected_date,
        'date_selection_form': date_selection_form,
    })

@login_required
def todays_submission_data(request):
    user = request.user
    fill_in_the_blanks_data = Intention.objects.filter(user=user, form_submission_date=timezone.localtime(timezone.now()).date()).order_by('-id').first()
    shift_data = Shift.objects.filter(user=user, form_submission_date=timezone.localtime(timezone.now()).date()).order_by('-id').first()

    return render(request, 'myapp/submitted_intention_today.html', {
        'intention_data': fill_in_the_blanks_data,
        'feeling': fill_in_the_blanks_data.feeling if fill_in_the_blanks_data else '',
        'action': fill_in_the_blanks_data.action if fill_in_the_blanks_data else '',
        'shift_data': shift_data,
        'user_input': request.GET.get('user_input', '')
    })

def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            # Extract cleaned data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            # Create user
            User.objects.create_user(username=username, password=password, email=email)

            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserSignUpForm()
    return render(request, 'myapp/registration/signup.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug information
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User is authenticated
            login(request, user)
            print("Authentication successful")
            return redirect('home_view')
        else:
            # Authentication failed
            print("Authentication failed")
            form = UserLoginForm()
            return render(request, 'myapp/registration/login.html', {'error': 'Invalid username or password', 'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'myapp/registration/login.html', {'form': form})

def retrieve_username(request):
    if request.method == 'POST':
        form = UsernameRetrievalForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            for user in users:
                # Send an email with the username
                send_mail(
                    'Username Retrieval',
                    f'Your username is: {user.username}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            return render(request, 'myapp/registration/username_retrieval_done.html')
    else:
        form = UsernameRetrievalForm()
    return render(request, 'myapp/registration/username_retrieval_form.html', {'form': form})
   

def test_email(request):
    try:
        send_mail(
            'Test Email',
            'This is a test email.',
            settings.EMAIL_HOST_USER,
            ['your-email@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {e}")



    

from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.user_login, name = 'home_login'),
    path('home_view/', views.home_view, name='home_view'),
    path('assessment_view/', views.assessment_view, name ='assessment_view'),
    path('selected_date/', views.selected_date_submission_results, name='selected_date_results'),
    path('submitted_assessment/', views.submitted_assessment, name='submitted_results'),
    path('submitted_intention/', views.todays_submission_data, name='submitted_intention'),
    path('signup/', views.user_signup, name='signup'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('retrieve_username/', views.retrieve_username, name='retrieve_username'),
   
    path('test-email/', views.test_email, name='test_email'),
]

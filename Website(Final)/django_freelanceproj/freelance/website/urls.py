from django.urls import path
from .views import *
from .views import login

urlpatterns = [
    path('', home_page, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('Freelancer_Dashboard/', freelance_dashbaord, name='Freelancer_Dashboard'),
    path('Client_Dashboard/', Client_dashboard, name='Client_Dashboard'),
    path('post_job/',post_job, name='post_job'),
    path('clientjob/',clientjob, name='clientjob'),
    path('find_work/',find_work, name='find_work'),
    path('Client_Edit/',Client_Edit, name='Client_Edit'),
    path('Post_Review/',post_review, name='Post_Review'),
    path('job_history/',job_history, name='job_history'),
    path('freelancer_history/',freelance_history, name='freelance_history'),
    path('freelancer_Edit/',freelancer_Edit, name='freelancer_Edit'),
]



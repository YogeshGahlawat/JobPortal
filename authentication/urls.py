from django.urls import path
from authentication.views import *

urlpatterns = [
    path('register/', renderRegister, name='register'),
    path('login/', renderLogin, name='login'),
    path('logout/', renderLogout, name='logout'),
    path('dashboard/', renderDashboard, name='dashboard'),
    path('profile/', userProfile, name='profile'),
    path('postJob/', postJob, name='postJob'),
    path('postedJobs/', postedJobs, name='postedJobs'),
    path('removeJob/', removeJob, name='removeJob'),
    path('candidateList/', candidateList, name='candidateList'),
    path('searchJob/', searchJob, name='searchJob'),
    path('applyJob/', applyJob, name='applyJob'),
    path('appliedJobs/', appliedJobs, name='appliedJobs'),
    path('withdrawApplication/', withdrawApplication, name='withdrawApplication'),
]
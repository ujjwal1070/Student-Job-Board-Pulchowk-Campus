from django.urls import path, include

from .views import *
from jobsapp import views

app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='searh'),
    path('candidate_search', CandidateSearchView.as_view(), name='candidate_search'),
    path('employer/dashboard', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
        path('applicant_profile/<int:id>', views.applicant_profile, name='applicant_profile'),
        path('edit-jobpost/<int:id>', views.JobUpdateView.as_view(), name='employer-edit-jobpost'),
        
    ])),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),
    #path('elasticsearch/',include('haystack.urls')),


    path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
    
]

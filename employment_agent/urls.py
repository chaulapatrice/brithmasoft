from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path('', employer_agent, name="home"),
    path("employers/", EmployersList.as_view(), name="employers"),
    path("employers/create/", EmployerCreateView.as_view(), name="create-employer"),
    path("employers/<pk>/delete/",
         EmployerDeleteView.as_view(), name="delete-employer"),
    path("employers/<pk>/", EmployerDetailView.as_view(), name="view-employer"),
    path("employers/<pk>/update/",
         EmployerUpdateView.as_view(), name="edit-employer"),
    path('employers/search/<page>/', search_employers, name="search-employers"),
    path("job_seekers/", JobSeekersList.as_view(), name="job-seekers"),
    path("job_seekers/create/", JobSeekerCreateView.as_view(),
         name="create-job-seeker"),
    path("job_seekers/<pk>/", JobSeekerDetailView.as_view(), name="view-job-seeker"),
    path("job_seekers/<pk>/update/",
         JobSeekerUpdateView.as_view(), name="edit-job-seeker"),
    path("job_seekers/<pk>/delete/",
         JobSeekerDeleteView.as_view(), name="delete-job-seeker"),
    path('job_seekers/search/<page>/',
         search_job_seekers, name="search-job-seekers"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

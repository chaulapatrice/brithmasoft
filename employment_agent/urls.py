from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', employer_agent, name="home"),
    path("employers/", EmployersList.as_view(), name="employers"),
    path("job_seekers/", job_seeker_index, name="job-seekers"),
    path("employers/<pk>/delete/", EmployerDeleteView.as_view(),name="delete-employer"),
    path("employers/<pk>/", EmployerDetailView.as_view(), name="view-employer"),
    path("employers/<pk>/update/", EmployerUpdateView.as_view(), name="edit-employer"),
    path('employers/search/<page>/', search_employers, name="search-employers")
]
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', employer_agent, name="home"),
    path("employers/", employers_index, name="employers"),
    path("job_seekers/", job_seeker_index, name="job-seekers")
]
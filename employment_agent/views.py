from django.shortcuts import render

# Create your views here.
def employer_agent(request):
    context = {}
    return render(request, "employment_agent/home.html", context)

def employers_index(request):
    context = {}
    return render(request, "employment_agent/employers_index.html", context)

def job_seeker_index(request):
    context = {}
    return render(request, "employment_agent/job_seekers_index.html", context)
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .models import *
from .forms import *
import re
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage

# Create your views here.
def employer_agent(request):
    context = {}
    return render(request, "employment_agent/home.html", context)

def mobile(request):
    """Return true if the request comes from a mobile device"""
    MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

class EmployersList(ListView):
    paginate_by = 10
    model = Employer
    context_object_name = "employers_list"
    template_name = "employment_agent/employers_index.html"
    ordering=['date_needed']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_mobile = False
        if mobile(self.request):
            is_mobile = True
        context['is_mobile'] = is_mobile
        context['search_url'] = reverse('search-employers', kwargs={'page':1})
        
        return context
   



class EmployerDeleteView(DeleteView):
    model = Employer
    #template_name = "employment_agent/employer_confirm_delete.html"
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_object().delete()
        payload = {"delete": "ok"}
        return JsonResponse(payload)

class EmployerDetailView(DetailView):
    model = Employer
    context_object_name = "employer"
    template_name = "employment_agent/employer_details.html"


class EmployerUpdateView(UpdateView):
    model = Employer
    fields = ['firstname', 'lastname', 'phone_number', 
    'physical_address', 'email_address', 'job_title', 'job_description', 
    'status', 'date_needed']
    template_name_suffix = '_update_form'
    context_object_name = "employer"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("view-employer", kwargs={"pk": pk})
    


              
        

def job_seeker_index(request):
    context = {}
    return render(request, "employment_agent/job_seekers_index.html", context)

#view to reset the page count when searching
def reset_page_count(request):
    page_number = request.session.get('page_number')
    if page_number is None:
        request.session['page_number'] = 1
    else:
        request.session['page_number'] = 1
    
    return JsonResponse({"message": "Successfully reseted page number"})

def search_employers(request, page):
    if request.method == "POST":
        form_data = json.loads(request.body)
        print(form_data)
        search_form = SearchForm(form_data or None)
        if search_form.is_valid():
            #do the searching 
            status = search_form.cleaned_data['status']
            if status == 1:
                status = True
            else:
                status = False

            job_title = search_form.cleaned_data['job_title']
            #save session data for the next search of the same type
            request.session['status'] = status
            request.session['job_title'] = job_title

            #want to search for employers with status and job_title that
            #matches the given query
            queryset = Employer.objects.filter(job_title__contains=job_title,status=status).order_by('job_title')
            
            #now paginate the data
            pages = Paginator(queryset, 10)
            

            #get the results
            results = pages.page(1)
            
            #json serialize the data
            data = serializers.serialize("json", results)
            content = {}
            content['data'] = data
            content['total_pages'] = pages.num_pages
            content['current_page'] = int(page)
            #set the next page to be viewed 
            if results.has_next():
                content['next_page'] = 2
            
            return JsonResponse(content)
        else:
            response = JsonResponse({"message": "Please provide valid input" })
            response.status_code = 400
            return response
    else:
        #Request is a GET
        status = request.session.get('status', None)
        job_title = request.session.get('job_title', None)
        #Make a query
        queryset = Employer.objects.filter(job_title__contains=job_title,status=status).order_by('job_title')
        #Paginate 
        pages = Paginator(queryset, 10)
        #get the results
        results = None
        try:
            results = pages.page(page)
        except InvalidPage:
            response = JsonResponse({"message": "Nothing found"})
            return response
        #set the content 
        content = {}
        content['data'] = serializers.serialize("json", results)
        content['total_pages'] = pages.num_pages
        content['current_page'] = int(page)
        #set the next page to be viewed
        if results.has_next():
            content['next_page'] = int(page) + 1
        #set the previous page
        if results.has_previous():
            content['previous_page'] = int(page) - 1
        
        return JsonResponse(content)
        



    
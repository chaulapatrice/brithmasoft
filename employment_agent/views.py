import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .models import *
from .forms import *
import re
from django.core import serializers
from django.core.paginator import Paginator, InvalidPage
from django.conf import settings

# Create your views here.


def employer_agent(request):
    context = {
        'nbar': 'home'
    }
    return render(request, "employment_agent/home.html", context)


def mobile(request):
    """Return true if the request comes from a mobile device"""
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)", re.IGNORECASE)
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


class EmployersList(ListView):
    paginate_by = 10
    model = Employer
    context_object_name = "employers_list"
    template_name = "employment_agent/employers_index.html"
    ordering = ['date_needed']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_mobile = False
        if mobile(self.request):
            is_mobile = True
        context['is_mobile'] = is_mobile
        context['form'] = EmployerFilterForm()
        context['search_url'] = reverse('search-employers', kwargs={'page': 1})
        context['nbar'] = 'employers'
        return context

    def get_queryset(self):
        qs = self.model.objects.all()
        form = EmployerFilterForm(self.request.GET)
        # check if form is valid
        if form.is_valid():
            # now make a search based on the form
            # fields provided
            if form.cleaned_data['job_title']:
                qs = qs.filter(job_title__contains=form.cleaned_data['job_title'])
            if form.cleaned_data['status']:
                qs = qs.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['firstname']:
                qs = qs.filter(firstname__contains=form.cleaned_data['firstname'])
            if form.cleaned_data['lastname']:
                qs = qs.filter(lastname__contains=form.cleaned_data['lastname'])

        return qs




class EmployerCreateView(CreateView):
    model = Employer
    form_class = EmployerForm

    # Redirect to view the newly created employer
    def get_success_url(self):
        return reverse('view-employer', kwargs={'pk': self.object.pk})


class EmployerDeleteView(DeleteView):
    model = Employer
    #template_name = "employment_agent/employer_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_object().delete()
        payload = {"delete": "ok"}
        return HttpResponseRedirect(reverse("employers"))


class EmployerDetailView(DetailView):
    model = Employer
    context_object_name = "employer"
    template_name = "employment_agent/employer_details.html"


class EmployerUpdateView(UpdateView):
    model = Employer
    form_class = EmployerForm
    template_name_suffix = '_update_form'
    context_object_name = "employer"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("view-employer", kwargs={"pk": pk})


# View for searching employers
def search_employers(request, page):
    if request.method == "POST":
        search_form = None
        if settings.TESTING:
            search_form = SearchEmployersForm(request.POST or None)
        else:
            form_data = json.loads(request.body)
            search_form = SearchEmployersForm(form_data or None)
        # Check if the form is valid
        if search_form.is_valid():
            # do the searching
            status = search_form.cleaned_data['status']
            if status == 1:
                status = True
            else:
                status = False

            job_title = search_form.cleaned_data['job_title']
            # save session data for the next search of the same type
            request.session['status'] = status
            request.session['job_title'] = job_title

            # want to search for employers with status and job_title that
            # matches the given query
            queryset = Employer.objects.filter(
                job_title__contains=job_title, status=status).order_by('job_title')

            # now paginate the data
            pages = Paginator(queryset, 10)

            # get the results
            results = pages.page(1)

            # json serialize the data
            data = serializers.serialize("json", results)
            content = {}
            content['data'] = data
            content['total_pages'] = pages.num_pages
            content['current_page'] = int(page)
            # set the next page to be viewed
            if results.has_next():
                content['next_page'] = 2

            return JsonResponse(content)
        else:
            response = JsonResponse({"message": "Please provide valid input"})
            response.status_code = 400
            return response
    else:
        # Request is a GET
        status = request.session.get('status', None)
        job_title = request.session.get('job_title', None)
        # Make a query
        queryset = Employer.objects.filter(
            job_title__contains=job_title, status=status).order_by('job_title')
        # Paginate
        pages = Paginator(queryset, 10)
        # get the results
        results = None
        try:
            results = pages.page(page)
        except InvalidPage:
            response = JsonResponse({"message": "Nothing found"})
            return response
        # set the content
        content = {}
        content['data'] = serializers.serialize("json", results)
        content['total_pages'] = pages.num_pages
        content['current_page'] = int(page)
        # set the next page to be viewed
        if results.has_next():
            content['next_page'] = int(page) + 1
        # set the previous page
        if results.has_previous():
            content['previous_page'] = int(page) - 1

        return JsonResponse(content)


# Job seeker list view
class JobSeekersList(ListView):
    paginate_by = 10
    model = JobSeeker
    context_object_name = "jobseekers_list"
    template_name = "employment_agent/job_seekers_index.html"
    ordering = ['date_applied']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        is_mobile = False
        if mobile(self.request):
            is_mobile = True
        context['is_mobile'] = is_mobile
        context['nbar'] = 'jobseekers'
        context['form'] = JobSeekerFilterForm()
        return context

    def get_queryset(self):
        qs = self.model.objects.all()
        form = JobSeekerFilterForm(self.request.GET)
        # check if form is valid
        if form.is_valid():
            # now make a search based on the form
            # fields provided
            if form.cleaned_data['job_title']:
                qs = qs.filter(job_title__contains=form.cleaned_data['job_title'])
            if form.cleaned_data['status']:
                qs = qs.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['firstname']:
                qs = qs.filter(firstname__contains=form.cleaned_data['firstname'])
            if form.cleaned_data['lastname']:
                qs = qs.filter(lastname__contains=form.cleaned_data['lastname'])

        return qs



# Job seeker detail view
class JobSeekerDetailView(DetailView):
    model = JobSeeker
    context_object_name = "jobseeker"
    template_name = "employment_agent/job_seeker_details.html"

# Job seeker create view


class JobSeekerCreateView(CreateView):
    model = JobSeeker
    form_class = JobSeekerForm

    # Redirect to view the newly created job seeker
    def get_success_url(self):
        return reverse('view-job-seeker', kwargs={'pk': self.object.pk})


class JobSeekerUpdateView(UpdateView):
    model = JobSeeker
    form_class = JobSeekerForm
    template_name_suffix = '_update_form'
    context_object_name = "jobseeker"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("view-job-seeker", kwargs={"pk": pk})

    '''
    def post(self, request, **kwargs):
        jobseeker_form = JobSeekerForm(request.POST, request.FILES)
        if jobseeker_form.is_valid():
            # First get the object referenced here
            jobseeker_form.save()
            # Redirect user to view the updated changes
            pk = int(self.kwargs["pk"])
            return HttpResponseRedirect(reverse("view-employer", kwargs={"pk": pk}))
        else:
            return render(request, "employment_agent/jobseeker_update_form.html", {"form": jobseeker_form})
    '''


class JobSeekerDeleteView(DeleteView):
    model = JobSeeker
    #template_name = "employment_agent/employer_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_object().delete()
        payload = {"delete": "ok"}
        return HttpResponseRedirect(reverse("job-seekers"))


# View for searching job seekers
def search_job_seekers(request, page):
    if request.method == "POST":
        search_form = None
        if settings.TESTING:
            search_form = SearchJobSeekersForm(request.POST or None)
        else:
            form_data = json.loads(request.body)
            search_form = SearchJobSeekersForm(form_data or None)
        # Check if the form is valid
        if search_form.is_valid():
            # do the searching
            status = search_form.cleaned_data['status']
            if status == 1:
                status = True
            else:
                status = False

            job_title = search_form.cleaned_data['job_title']
            # save session data for the next search of the same type
            request.session['job_seeker_status'] = status
            request.session['job_seeker_job_title'] = job_title

            # want to search for employers with status and job_title that
            # matches the given query
            queryset = JobSeeker.objects.filter(
                job_title__contains=job_title, status=status).order_by('job_title')

            # now paginate the data
            pages = Paginator(queryset, 10)

            # get the results
            results = pages.page(1)

            # json serialize the data
            data = serializers.serialize("json", results)
            content = {}
            content['data'] = data
            content['total_pages'] = pages.num_pages
            content['current_page'] = int(page)
            # set the next page to be viewed
            if results.has_next():
                content['next_page'] = 2

            return JsonResponse(content)
        else:
            response = JsonResponse({"message": "Please provide valid input"})
            response.status_code = 400
            return response
    else:
        # Request is a GET
        status = request.session.get('job_seeker_status', None)
        job_title = request.session.get('job_seeker_job_title', None)
        # Make a query
        queryset = JobSeeker.objects.filter(
            job_title__contains=job_title, status=status).order_by('job_title')
        # Paginate
        pages = Paginator(queryset, 10)
        # get the results
        results = None
        try:
            results = pages.page(page)
        except InvalidPage:
            response = JsonResponse({"message": "Nothing found"})
            return response
        # set the content
        content = {}
        content['data'] = serializers.serialize("json", results)
        content['total_pages'] = pages.num_pages
        content['current_page'] = int(page)
        # set the next page to be viewed
        if results.has_next():
            content['next_page'] = int(page) + 1
        # set the previous page
        if results.has_previous():
            content['previous_page'] = int(page) - 1

        return JsonResponse(content)

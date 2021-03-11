from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from employment_agent.models import *
from django.utils.dateparse import parse_date
import json
import time
import os


class TestViews(TestCase):

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0")
        self.url = reverse("home")
        date_str = "2020-09-15"
        temp_date = parse_date(date_str)
        # Create a list of employer objects
        Employer.objects.create(
            firstname="Patrice",
            lastname="Chaula",
            phone_number="+263782841339",
            physical_address="4790 Mkoba 12, Gweru, Midlands",
            email_address="chaulapsx@gmail.com",
            job_title="Carpenter to create me something",
            job_description="I am searching for a carpenter to create me something.",
            status=False,
            date_needed=temp_date
        )

        date_str = "2020-09-20"
        temp_date = parse_date(date_str)

        Employer.objects.create(
            firstname="John",
            lastname="Doe",
            phone_number="+263782841339",
            physical_address="4790 Mkoba 12, Gweru, Midlands",
            email_address="johndoe@gmail.com",
            job_title="Motor mechanic for engine overhaul",
            job_description="I am currently looking for a motor mechanic for my engine overhaul.",
            status=False,
            date_needed=temp_date
        )
        # Create a list of job seeker objects
        JobSeeker.objects.create(
            firstname="Patrice",
            lastname="Chaula",
            phone_number="+263782841339",
            physical_address="4790 Mkoba 12, Gweru, Midlands",
            email_address="chaulapsx@gmail.com",
            job_title="Carpenter to create me something",
            status=False,
            date_applied=temp_date
        )

        date_str = "2020-09-20"
        temp_date = parse_date(date_str)

        JobSeeker.objects.create(
            firstname="John",
            lastname="Doe",
            phone_number="+263782841339",
            physical_address="4790 Mkoba 12, Gweru, Midlands",
            email_address="johndoe@gmail.com",
            job_title="Motor mechanic for engine overhaul",
            status=False,
            date_applied=temp_date
        )

    # Test if the homepage is accessible and using the right template

    def test_employer_agent(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "employment_agent/home.html")

    # Test if the employers index page is reachable and is using the right template
    def test_employers_index_page_get(self):
        response = self.client.get(reverse("employers"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, "employment_agent/employers_index.html")

    # Test create employer data
    def test_create_employer_data(self):
        url = reverse("create-employer")
        date_str = "2020-09-20"
        temp_date = parse_date(date_str)
        # Open a file to upload on post
        with open('test_data/Resume.docx', 'rb') as resume:
            # Send a post request
            response = self.client.post(url, {
                'firstname': 'John',
                'lastname': 'Doe',
                'phone_number': '07777777',
                'physical_address': '22 Fake Street',
                'job_title': 'I want a person to cut my hedge',
                'job_description': 'I want my hedge to be cut really nice',
                'status': False,
                'date_needed': '2020-09-20',
                'resume': resume
            })
            # Check if the employer data was created
            self.assertEquals(Employer.objects.last().firstname, 'John')

    # Test if the employer data can be deleted successfully
    def test_delete_employer_data(self):
        url = reverse("delete-employer", kwargs={"pk": 1})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 302)

    # Test what happens if we try to delete data that do not exist
    def test_delete_employer_data_does_not_exist(self):
        url = reverse("delete-employer", kwargs={"pk": 9})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 404)

    # Test if specific employer data is viewable
    def test_view_employer_data(self):
        url = reverse("view-employer", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertContains(response, "Patrice")
        self.assertContains(response, "Chaula")
        self.assertContains(response, "Carpenter to create me something")

    # Test try to view employer data that does not exist

    def test_view_employer_data_does_not_exist(self):
        url = reverse("view-employer", kwargs={"pk": 9})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # Test searching employer data
    def test_search_employers(self):
        url = reverse("search-employers", kwargs={"page": 1})
        response = self.client.post(
            url, {"status": 0, "job_title": "to create"})

        # Check if the right data is contained in the response
        self.assertContains(response, "Carpenter to create me something")

        # now test a GET request ie searching using session data
        response = self.client.get(url)
        # Check if the right data is contained in the response
        self.assertContains(response, "Carpenter to create me something")

    # Test create employer data
    def test_create_job_seeker_data(self):
        url = reverse("create-job-seeker")
        date_str = "2020-09-20"
        temp_date = parse_date(date_str)
        # Open a file to upload on post
        with open('test_data/Resume.docx', 'rb') as resume:
            # Send a post request
            response = self.client.post(url, {
                'firstname': 'John',
                'lastname': 'Doe',
                'phone_number': '07777777',
                'physical_address': '22 Fake Street',
                'job_title': 'I want a person to cut my hedge',
                'status': False,
                'date_applied': '2020-09-20',
                'resume': resume
            })
            # Check if the employer data was created
            self.assertEquals(JobSeeker.objects.last().firstname, 'John')

    # Test if specific job seeker data is viewable
    def test_view_job_seeker_data(self):
        url = reverse("view-job-seeker", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertContains(response, "Patrice")
        self.assertContains(response, "Chaula")
        self.assertContains(response, "Carpenter to create me something")

    # Test delete job seeker data
    def test_delete_job_seeker_data(self):
        url = reverse("delete-job-seeker", kwargs={"pk": 2})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 302)

     # Test searching employer data
    def test_search_job_seekers(self):
        url = reverse("search-job-seekers", kwargs={"page": 1})
        response = self.client.post(
            url, {"status": 0, "job_title": "to create"})

        # Check if the right data is contained in the response
        self.assertContains(response, "Carpenter to create me something")

        # now test a GET request ie searching using session data
        response = self.client.get(url)
        # Check if the right data is contained in the response
        self.assertContains(response, "Carpenter to create me something")

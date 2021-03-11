from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.utils.dateparse import parse_date
from employment_agent.models import *
from employment_agent.fakers import *
import json
from django.urls import reverse
import time


class TestEmployerPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0")
        self.url = reverse("home")
        # Create a list of employer objects
        #fake_employers = EmployerFaker(20)
        #Create a list of job seeker objects
        #fake_job_seekers = JobSeekerFaker(20)
        date_str = "2020-09-15"
        temp_date = parse_date(date_str)
        # Create a list of employer objects
        Employer.objects.create(
            firstname="Patrice",
            lastname="Chaula",
            phone_number="+263782841339",
            physical_address="4790 Mkoba 12, Gweru, Midlands",
            email_address="chaulapsx@gmail.com",
            job_title="Carpenter to adjust my kitchen unit",
            job_description="I am searching for a carpenter to fix my kitchen unit.",
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





    def tearDown(self):
        self.browser.close()

    def test_job_seeker_url_goes_to_job_seekers(self):
        self.browser.get(self.live_server_url)

        # The user requests the page
        job_seeker_url = self.live_server_url + reverse("job-seekers")
        self.browser.find_element_by_id("go-to-job-seekers").click()

        self.assertEquals(
            self.browser.current_url,
            job_seeker_url
        )

    def test_employer_url_goes_to_employers(self):
        self.browser.get(self.live_server_url)

        # The user requests the page
        employer_url = self.live_server_url + reverse("employers")
        self.browser.find_element_by_id("go-to-employers").click()

        self.assertEquals(
            self.browser.current_url,
            employer_url
        )

    def test_edit_employer_data(self):
        url = self.live_server_url + reverse("edit-employer", kwargs={"pk": 1})
        self.browser.get(url)
        self.browser.find_element_by_id("id_firstname").clear()
        self.browser.find_element_by_id("id_firstname").send_keys("Tapiwa")
        self.browser.find_element_by_id("id_lastname").clear()
        self.browser.find_element_by_id("id_lastname").send_keys("Chikerema")
        self.browser.find_element_by_id("update-btn").click()
        employer = Employer.objects.get(id=1)
        self.assertEquals(employer.firstname, "Tapiwa")
        self.assertEquals(employer.lastname, "Chikerema")

    def test_edit_job_seeker_data(self):

         # Create a list of job seeker objects
        date_str = "2020-09-20"
        temp_date = parse_date(date_str)

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

        url = self.live_server_url + reverse("edit-job-seeker", kwargs={"pk": 1})
        self.browser.get(url)
        self.browser.find_element_by_id("id_firstname").clear()
        self.browser.find_element_by_id("id_firstname").send_keys("Tapiwa")
        self.browser.find_element_by_id("id_lastname").clear()
        self.browser.find_element_by_id("id_lastname").send_keys("Chikerema")
        self.browser.find_element_by_id("update-btn").click()
        jobseeker = JobSeeker.objects.get(id=1)
        self.assertEquals(jobseeker.firstname, "Tapiwa")
        self.assertEquals(jobseeker.lastname, "Chikerema")

from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from employment_agent.models import *
from django.utils.dateparse import parse_date
import json
import time


class TestViews(TestCase):

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT="Mozilla/5.0")
        self.url = reverse("home")
        date_str = "2020-09-15"
        temp_date = parse_date(date_str)
        #Create a list of employer objects
        Employer.objects.create(
            firstname = "Patrice",
            lastname = "Chaula",
            phone_number = "+263782841339",
            physical_address = "4790 Mkoba 12, Gweru, Midlands",
            email_address = "chaulapsx@gmail.com",
            job_title = "Carpenter to adjust my kitchen unit",
            job_description = "I am searching for a carpenter to fix my kitchen unit.",
            status=False,
            date_needed=temp_date
        )

        date_str = "2020-09-20"
        temp_date = parse_date(date_str)

        Employer.objects.create(
            firstname = "John",
            lastname = "Doe",
            phone_number = "+263782841339",
            physical_address = "4790 Mkoba 12, Gweru, Midlands",
            email_address = "johndoe@gmail.com",
            job_title = "Motor mechanic for engine overhaul",
            job_description = "I am currently looking for a motor mechanic for my engine overhaul.",
            status=False,
            date_needed=temp_date
        )
    
    
    #Test if the homepage is accessible and using the right template
    def test_employer_agent(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "employment_agent/home.html")

    #Test if the employers index page is reachable and is using the right template
    def test_employers_index_page_get(self):
        response = self.client.get(reverse("employers"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "employment_agent/employers_index.html")

    #Test if the employer data can be deleted successfully
    def test_delete_employer_data(self):
        url = reverse("delete-employer", kwargs={"pk": 1})
        response = self.client.post(url)
        data = json.loads(response.content)
        self.assertEquals(data["delete"], "ok")

    #Test what happens if we try to delete data that do not exist
    def test_delete_employer_data_does_not_exist(self):
        url = reverse("delete-employer", kwargs={"pk": 9})
        response = self.client.post(url)
        self.assertEquals(response.status_code, 404)

    #Test if specific employer data is viewable
    def test_view_employer_data(self):
        url = reverse("view-employer", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertContains(response, "Patrice")
        self.assertContains(response, "Chaula")
        self.assertContains(response, "Carpenter to adjust my kitchen unit")

    #Test try to view employer data that does not exist
    def test_view_employer_data_does_not_exist(self):
        url = reverse("view-employer", kwargs={"pk": 9})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)
    
   
    
class TestViewsLiveServer(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        date_str = "2020-09-15"
        temp_date = parse_date(date_str)
        #Create a list of employer objects
        Employer.objects.create(
            firstname = "Patrice",
            lastname = "Chaula",
            phone_number = "+263782841339",
            physical_address = "4790 Mkoba 12, Gweru, Midlands",
            email_address = "chaulapsx@gmail.com",
            job_title = "Carpenter to adjust my kitchen unit",
            job_description = "I am searching for a carpenter to fix my kitchen unit.",
            status=False,
            date_needed=temp_date
        )

        date_str = "2020-09-20"
        temp_date = parse_date(date_str)

        Employer.objects.create(
            firstname = "John",
            lastname = "Doe",
            phone_number = "+263782841339",
            physical_address = "4790 Mkoba 12, Gweru, Midlands",
            email_address = "johndoe@gmail.com",
            job_title = "Motor mechanic for engine overhaul",
            job_description = "I am currently looking for a motor mechanic for my engine overhaul.",
            status=False,
            date_needed=temp_date
        )

    def tearDown(self):
        self.browser.close()
    
    def test_edit_employer_data(self):
        url = self.live_server_url + reverse("edit-employer", kwargs={"pk": 1})
        self.browser.get(url)
        self.browser.find_element_by_id("id_firstname").clear()
        self.browser.find_element_by_id("id_firstname").send_keys("Tapiwa")
        self.browser.find_element_by_id("id_lastname").clear()
        self.browser.find_element_by_id("id_lastname").send_keys("Chikerema")
        self.browser.find_element_by_id("update-btn").click()
        employer  = Employer.objects.get(id=1)
        self.assertEquals(employer.firstname, "Tapiwa")
        self.assertEquals(employer.lastname, "Chikerema")
    

    
    


    
        
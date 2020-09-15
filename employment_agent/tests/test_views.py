from django.test import TestCase, Client
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse("home")
    

    def test_employer_agent(self):
        client = Client()
        response = client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "employment_agent/home.html")
    
        
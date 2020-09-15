from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time

class TestEmployerPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.close()
    
    def test_job_seeker_url_goes_to_job_seekers(self):
        self.browser.get(self.live_server_url)
        
        #The user requests the page
        job_seeker_url = self.live_server_url + reverse("job-seekers")
        self.browser.find_element_by_id("go-to-job-seekers").click()
        
        self.assertEquals(
            self.browser.current_url,
            job_seeker_url
        )
    
    def test_employer_url_goes_to_employers(self):
        self.browser.get(self.live_server_url)

        #The user requests the page
        employer_url = self.live_server_url + reverse("employers")
        self.browser.find_element_by_id("go-to-employers").click()
        
        self.assertEquals(
            self.browser.current_url,
            employer_url
        )


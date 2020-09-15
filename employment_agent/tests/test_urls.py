from django.test import SimpleTestCase
from django.urls import reverse, resolve
from employment_agent.views import *

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func, employer_agent)
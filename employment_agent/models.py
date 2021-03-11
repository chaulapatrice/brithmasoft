from django.db import models
from .helpers import RandomFileName
# Create your models here.


class Employer(models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=13)
    physical_address = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=90)
    job_title = models.CharField(max_length=500)
    job_description = models.CharField(max_length=4000)
    status = models.BooleanField(default=False)
    date_needed = models.DateField()
    resume = models.FileField(upload_to=RandomFileName(
        "employer_files"), default="employer_files/Resume.docx")

    def __str__(self):
        return self.firstname + " " + self.lastname


class JobSeeker(models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=13)
    email_address = models.EmailField(max_length=45)
    physical_address = models.CharField(max_length=255)
    job_title = models.CharField(max_length=500)
    description = models.CharField(max_length=4000)
    status = models.BooleanField(default=False)
    date_applied = models.DateField()
    resume = models.FileField(upload_to=RandomFileName(
        "job_seeker_files"), default="job_seeker_files/Resume.docx")

    def __str__(self):
        return self.firstname + " " + self.lastname

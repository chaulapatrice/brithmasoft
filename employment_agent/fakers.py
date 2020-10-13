from faker import Faker
from .models import Employer, JobSeeker
import uuid

class EmployerFaker:
    def __init__(self, count):
        fake = Faker()
        first_names = [fake.unique.first_name() for i in range(count)]
        last_names = [fake.unique.last_name() for i in range(count)]
        phone_numbers = [fake.unique.phone_number() for i in range(count)]
        addresses = [fake.unique.address() for i in range(count)]
        emails = [fake.unique.email() for i in range(count)]
        job_titles = [fake.unique.sentence() for i in range(count)]
        job_descriptions = [fake.unique.sentence() for i in range(count)]
        statuses = [fake.boolean() for i in range(count)]
        dates_needed = [fake.date() for i in range(count)]
        attachments = [uuid.uuid4() for i in range(count)]

        for i in range(count):
            Employer.objects.create(
                firstname = first_names[i],
                lastname = last_names[i],
                phone_number = phone_numbers[i],
                physical_address = addresses[i],
                email_address = emails[i],
                job_title = job_titles[i],
                job_description = job_descriptions[i],
                status = statuses[i],
                date_needed = dates_needed[i],
                attachments_file_name = attachments[i]
            )


        
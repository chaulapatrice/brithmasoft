# Generated by Django 3.1.2 on 2020-10-15 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employment_agent', '0003_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobseeker',
            name='attachments_file_name',
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='resume',
            field=models.FileField(default='employer_files/Resume.docx', upload_to='employer_files'),
        ),
    ]

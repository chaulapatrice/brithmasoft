# Generated by Django 3.1.2 on 2020-10-15 22:49

from django.db import migrations, models
import employment_agent.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('employment_agent', '0004_auto_20201015_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='resume',
            field=models.FileField(default='employer_files/Resume.docx', upload_to=employment_agent.helpers.RandomFileName('employer_files')),
        ),
    ]

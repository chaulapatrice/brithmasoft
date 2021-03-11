from django import forms
from .models import *

# To be used with status field
TRUE_FALSE_CHOICES = (
    (True, 'Occupied'),
    (False, 'Vaccant')
)

EMPLOYED_UNEMPLOYED_CHOICES = (
    (True, 'Employed'),
    (False, 'Unemployed')
)

# The form for searching employers


class SearchEmployersForm(forms.Form):
    job_title = forms.CharField(max_length=500)
    status = forms.IntegerField()


class SearchJobSeekersForm(forms.Form):
    job_title = forms.CharField(max_length=500)
    status = forms.IntegerField()

# the form updating employer data


class EmployerForm(forms.ModelForm):
    status = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Status",
                               initial='', widget=forms.Select(), required=True)

    class Meta:
        model = Employer
        fields = ['firstname',
                  'lastname',
                  'phone_number',
                  'physical_address',
                  'email_address',
                  'job_title',
                  'job_description',
                  'status',
                  'date_needed',
                  'resume'
                  ]
        widgets = {
            'job_description': forms.Textarea(attrs={'rows': 5}),
            'firstname': forms.TextInput(attrs={'placeholder': 'Firstname'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Lastname'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+123456789012'}),
            'physical_address': forms.TextInput(attrs={'placeholder': '1234 Street 1'}),
            'email_address': forms.TextInput(attrs={'placeholder': 'jobseeker@example.com'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'Job title'})
        }


class EmployerFilterForm(forms.Form):
    firstname = forms.CharField(max_length=45, required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Firstname'
        }
    ))
    lastname = forms.CharField(max_length=45, required=False,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Lastname'
                               })
                               )
    job_title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Job title'
        }
    ))
    status = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Status",
                               initial='', widget=forms.Select(), required=False)
    date_needed = forms.DateField(required=False)


class JobSeekerFilterForm(forms.Form):
    firstname = forms.CharField(max_length=45, required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Firstname'
        }
    ))
    lastname = forms.CharField(max_length=45, required=False,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Lastname'
                               })
                               )
    job_title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Job title'
        }
    ))
    status = forms.ChoiceField(choices=EMPLOYED_UNEMPLOYED_CHOICES, label="Status",
                               initial='', widget=forms.Select(), required=False)

    date_applied = forms.DateField(required=False)


class JobSeekerForm(forms.ModelForm):
    status = forms.ChoiceField(choices=EMPLOYED_UNEMPLOYED_CHOICES, label="Status",
                               initial='', widget=forms.Select(), required=True)

    class Meta:
        model = JobSeeker
        fields = ['firstname',
                  'lastname',
                  'phone_number',
                  'physical_address',
                  'email_address',
                  'job_title',
                  'status',
                  'date_applied',
                  'resume'
                  ]
        widgets = {
            'firstname': forms.TextInput(attrs={'placeholder': 'Firstname'}),
            'lastname': forms.TextInput(attrs={'placeholder': 'Lastname'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+123456789012'}),
            'physical_address': forms.TextInput(attrs={'placeholder': 'Street address'}),
            'email_address': forms.TextInput(attrs={'placeholder': 'jobseeker@example.com'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'Job title'})
        }

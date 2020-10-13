from django import forms

class SearchForm(forms.Form):
    job_title = forms.CharField(max_length=500)
    status = forms.IntegerField()
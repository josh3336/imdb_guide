from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    zipcode= USZipCodeField()

class ZipCodeForm(forms.Form):
    zipcode= USZipCodeField()

class channels2filter(forms.Form):
	HBO= forms.BooleanField(required=False)
	Sho= forms.BooleanField(required=False)
	Starz= forms.BooleanField(required=False)
	MAX= forms.BooleanField(required=False)
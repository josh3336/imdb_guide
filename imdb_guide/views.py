
from django.shortcuts import render_to_response

from django.shortcuts import render,redirect
from titles.models import Titles
from django.http import HttpResponseRedirect, HttpResponse

from titles.views import guide, guide_filtered
from imdb_guide.forms import ContactForm,ZipCodeForm
from django.utils import simplejson


import datetime
import os
import sys

#import pickle
#sys.path.append('C:/Users/josh/Documents/coding/django_stuff/imdb_guide/helperfunctions')
#sys.path.append('C:/Users/josh/Documents/coding/django_stuff/imdb_guide/static/python')
#sys.path.append('C:/Users/josh/Documents/coding/moviesite/main_scripts/')
sys.path.append('/Users/hackreactor/code/josh3336/imdb_guide/static/python')
import imdbwithguide
import tvguide_helperfunctions




def home(request):
    """renders base.html
    """
    return render(request, 'base.html')


def findproviders(request):
    """used to call return_providers when zipcode is entered, returns a list of providers in json format"""
    zipcode = request.GET.get('zipcode')
    if zipcode is None:
        return HttpResponseBadRequest()
    providers=tvguide_helperfunctions.return_providers(zipcode)
    json = simplejson.dumps(providers)
    return HttpResponse(json, mimetype='application/json')

def about(request):
    """renders about.html
    """
    return render(request,'about.html')



def entered(request):
    """Called when user selects a provider. This uses the input to run a script which adds a specific tv guide to
    the database, then redirects the page to /guide
    """
    
    zipcode=request.GET['zipcode']
    headend=request.GET['headend']
    channel_filter=request.GET
    token=request.COOKIES["csrftoken"]
    now = datetime.datetime.now()
    imdbwithguide.main(zipcode,headend,token)
    return redirect("/guide")



def contact(request):
    """Contact form, which allows users to get in contact with web master"""
    now = datetime.datetime.now()
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients=['joshuapagano@gmail.com']
           # Next 2 lines: used for sending emails
           # from django.core.mail import send_mail
           # send_mail(subject,message,sender,recipients)
            message="Your email has been submitted. Thank You."
            return render(request, 'base.html', {"current_date": now, 'message':message})# Redirect after POST
    else:
        form = ContactForm() # An unbound form
    return render(request, 'contact.html', {
        'form': form, "current_date": now})
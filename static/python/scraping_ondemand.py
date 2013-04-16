 # -*- coding: utf-8 -*-
import urllib2
import re
import sys
import os

from BeautifulSoup import BeautifulSoup        
import simplejson as json#used for storing data in json format
import jsonpickle
import xmllib#for parsing html from code to ascii
import logging

#used for linking django testsite with project
sys.path.append('C:/Users/josh/Documents/coding/django_stuff/testsite2/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsite2.settings")
from titles.models import Ondemand_Titles#import django 


logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - %(message)s')
SHOWS=[]
ondemand_guide=[]

class OnDemand_Guide:
    def __init__(self,title,channel):

        self.title=title
        self.channel=channel
        #self.length=length
        self.score=None
        self.uservotes=None
        self.url=None
        self.showtype=None
        #self.zipcode=zip
        #self.headend=headend

def hbo_ondemand():
    """goes to hbo on demand page and finds all movie titles currently on demand and returns the list"""
    title_list=[]
    p=urllib2.urlopen("http://www.hboondemand.com/apps/hodschedule/hod/category.do?CATG_ID=BTRS302")
    urlcontents=str(p.read())
    alltitlesfound=re.findall(r'default_link">[A-Z][^<]+',urlcontents)
    for title in alltitlesfound:
        title_list.append([title[14:],'HBO'])
    
    p=urllib2.urlopen("http://www.hboondemand.com/apps/hodschedule/hod/category.do?CATG_ID=PMRS14242")
    urlcontents=str(p.read())
    alltitlesfound=re.findall(r'default_link">[A-Z][^<]+',urlcontents)
    for title in alltitlesfound:
        title_list.append([title[14:],'HBO'])
    return title_list

def sho_ondemand():
    """goes to showtime on demands page and finds all showtime movies currently on demand , filters out 
    coming soon titles, and returns the list"""
    title_list=[]
    status_list=[]
    title_list_on=[]
    title_to_status={}
    
    p=urllib2.urlopen("http://www.sho.com/sho/schedules/ondemand/movies#/index")
    urlcontents=str(p.read())
    alltitlesfound=re.findall(r'title" : "[^"]+',urlcontents)
    for title in alltitlesfound:
        title_list.append(title[10:])
        
    statusofmovies=re.findall(r'status" : "[^"]+',urlcontents)
    
    for status in statusofmovies:
        status_list.append(status[11:])
    
    for a in xrange(0,len(title_list)-2):
        title_to_status[title_list[a]]=status_list[a]
        
    for (key,value) in title_to_status.iteritems():
        if title_to_status[key]!="COMING_SOON":
            title_list_on.append([key,'SHO'])

    return title_list_on

def starz_ondemand():
    """goes to starz on demand page finds all on demand movies and returns the list"""
    title_list=[]
    p=urllib2.urlopen("http://www.starz.com/schedule/ondemandlistings/sod?filter=ALL")
    urlcontents=str(p.read())
    soup = BeautifulSoup(''.join(str(urlcontents)))
    segment=soup.find('div',{'class':"results"})
    titles_odd=soup.findAll('tr',{'class':'odd'})
    titles_even=soup.findAll('tr',{'class':'even'})
    for a in titles_odd:
        title=re.search(r'class="">[^<]+',str(a))
        if title:
            title_list.append([title.group()[9:],'STARZ'])
    for a in titles_even:
        title=re.search(r'class="">[^<]+',str(a))
        if title:
            title_list.append([title.group()[9:],'STARZ'])
    return title_list

def encore_ondemand():
    """goes to encore on demand page finds all on demand movies and returns the list"""
    title_list=[]
    p=urllib2.urlopen("http://www.starz.com/schedule/ondemandlistings/eoda?filter=ALL")
    urlcontents=str(p.read())
    soup = BeautifulSoup(''.join(str(urlcontents)))
    #print soup.prettify()
    segment=soup.find('div',{'class':"results"})
    titles_odd=soup.findAll('tr',{'class':'odd'})
    titles_even=soup.findAll('tr',{'class':'even'})
    for a in titles_odd:
        title=re.search(r'class="">[^<]+',str(a))
        if title:
            title_list.append([title.group()[9:],'ENCORE'])
    for a in titles_even:
        title=re.search(r'class="">[^<]+',str(a))
        if title:
            title_list.append([title.group()[9:],'ENCORE'])
    return title_list

def max_ondemand():
    """goes to cinemax on demand page finds all on demand movies and returns the list"""
    title_list=[]
    p=urllib2.urlopen("http://www.cinemax.com/apps/hodschedule/cod/")
    urlcontents=str(p.read())
    if 'META HTTP-EQUIV="Refresh"' in urlcontents:
        print 'Redirecting'
        meta_url=urlcontents.split('URL=')
        url_2redirect=meta_url[1].rstrip()
        p=urllib2.urlopen(url_2redirect[:-2])
        urlcontents=str(p.read())
    soup = BeautifulSoup(''.join(str(urlcontents)))
    segments=soup.findAll('td',{'class':"schedule-program-title"})
    for segment in segments:
        title=re.search(r'>[^<]+',str(segment))
        if title:
            if [title.group()[1:],'MAX'] not in title_list:
                title_list.append([title.group()[1:],'MAX'])
    return title_list

def loadjson():
    """loads json"""
    global SHOWS
    #loads SHOWS
    with open('C:/Users/josh/Documents/coding/moviesite/newdb_data/shows_asdict_updated.txt','rb') as outfile:
        SHOWS=json.load(outfile)
        
def make_hash():
    """returns a hashed dictionary using SHOWS in order to quickly sort through them at a later point"""
    global SHOWS
    showtypematch={"TV Series":'tv','TV Movie':'movie',"Mini-Series":'tv',"Movie":'movie'}
    
    print "Length of SHOWS: %s"%(len(SHOWS))
    char_tosub='[.!:;\'\ &*\(\)\-\?\,]|and|the'
    shows_hashed=dict((re.sub(char_tosub,'',d['title'].lower()),d) for d in SHOWS)
    
    print "Length of SHOWS_hashed: %s"%(len(shows_hashed))

    return shows_hashed

def check_for_match(hashed,guide):
    """accepts a hashed dictionary of loaded imdb shows and a list of Guide class objects,
    it then checks each objects.title to see if it matches a title in the hashed dictionary, if so it
    then appends the imdb information to the object , adds these objects to a list and returns the list"""

    shows_on=[]
    for a in guide:
        title_reduced=re.sub('[.!:;\'\ &*\(\)\-\?\,]|and|the','',a.title.lower())
        #print title_reduced
        if  title_reduced in hashed:
            #shows_on.append(hashed[title_reduced]['title'])
            a.url=hashed[title_reduced]['url']
            a.score=hashed[title_reduced]['imdb_score']
            a.uservotes=hashed[title_reduced]['uservotes']
            a.showtype=hashed[title_reduced]['showtype']
            shows_on.append(a)
    print "Matches in hashed guide plus re.sub:%s Titles:%s"%(len(shows_on),shows_on)
    return shows_on
    
def add2_ondemandguide(*args):
    """takes an optional number of arguments, each a list of title and channel pairs, and adds them to the class of 
    OnDemand_Guide"""
    for ar in args:
        for a in ar:
            ondemand_guide.append(OnDemand_Guide(a[0],a[1]))
    print "Titles in ondemand_guide:%s"%(len(ondemand_guide))
    return ondemand_guide


def addguide_2db(guidelist):
    """takes a guidelist runs checkguide, sorts it then adds the guide to the django db"""
    Ondemand_Titles.objects.all().delete()
    print "Adding titles to database"
    print len(guidelist)
    objects=[]
    for a in guidelist:
        objects.append(Ondemand_Titles(title=a.title, imdb_score=a.score, user_votes=a.uservotes, channel=a.channel, imdb_url=a.url,showtype=a.showtype))

    Ondemand_Titles.objects.bulk_create(objects)

def main():
    loadjson()
    hbo=hbo_ondemand()
    sho=sho_ondemand()
    starz=starz_ondemand()
    encore=encore_ondemand()
    cinemax=max_ondemand()
    ondemand_guide=add2_ondemandguide(hbo,sho,starz,encore,cinemax)
    hashed=make_hash()
    shows_on=check_for_match(hashed,ondemand_guide)
    addguide_2db(shows_on)
    

        
if __name__=='__main__': 
    #cProfile.run("main()")
    main()

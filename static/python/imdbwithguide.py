 # -*- coding: utf-8 -*-
import re
import mechanize

import os 
import sys
import xmllib#for parsing html from code to ascii
import logging #enables the logging module which is used for debugging
import cookielib#used for storing cookies while doing urllib2 imports
import simplejson as json#used for storing data in json format
import cProfile#used for profiling time of program


import urllib
import urllib2


from datetime import datetime#used in converting string time to date object
from BeautifulSoup import BeautifulSoup as bs_parse
from BeautifulSoup import BeautifulSoup        



sys.path.append('C:/Users/josh/Documents/coding/django_stuff/imdb_guide/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imdb_guide.settings")
from titles.models import Titles#import django 

#log in txt file
#logging.basicConfig(filename='C:\Users\josh\Documents\coding\moviesite\mainwithoutsearchterm\log_lastworking.txt', level='CRITICAL', format='%(asctime)s - %(levelname)s - %(message)s')

#log to console
logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - %(message)s')
#logging.basicConfig(level='CRITICAL', format='%(asctime)s - %(levelname)s - %(message)s')


br = mechanize.Browser()
br.set_handle_robots(False)

titles=[]
guide=[]
IMDB_SHOWS=[]

#Guide Class-used for tvguide
class Guide:
    def __init__(self,title,channel,time,length,typematch,zip,headend):

        self.title=title
        self.channel=channel
        self.time=datetime.strptime(time, '%I:%M%p')
        self.length=length
        self.score=None
        self.uservotes=None
        self.url=None
        self.showtype=typematch
        self.zipcode=zip
        self.headend=headend
            
    def __lt__(self, other):
        #used for sorting the class
        return self.score > other.score
    

#Show class-used for IMDB Shows
class Imdb_Show:
    def __init__(self,title,imdb_score,uservotes,url,year,showtype):
        self.title=title.strip()
        self.imdb_score=imdb_score
        self.uservotes=uservotes
        self.url=url
        self.year=year
        self.showtype=showtype

        
    def __lt__(self, other):
        #used for sorting the class
        return self.score > other.score


def condense_guide():
    """goes through guide list , removing elements that will not have a imdb score"""
    global guide
    indices_2delete=[]
    indices_of_titles=[]
    #removes term if anywhere in title
    term=['MLB','Sports','News', 'ROME','Hockey','NHL','NFL','NBA','UFC','Music','B1G','College Hoops','Skiing','Weather','Cycling','Big Ten','NASCAR','Boxing','BBC','ABC','Basketball','Football','Baseball','News at','Regular Programming']
    
    for a in term:
        for b in guide:
            if a in b.title:
                logging.debug("condense_guide: removing %s from titles that match term list"% b.title)
                indices_2delete.append(guide.index(b))
    guide = [i for j, i in enumerate(guide) if j not in indices_2delete]

def loadjson():
    """loads json"""
    global IMDB_SHOWS
    
    #loads IMDB_SHOWS
    with open('C:/Users/josh/Documents/coding/moviesite/newdb_data/shows_asdict_updated.txt','rb') as outfile:
        IMDB_SHOWS=json.load(outfile)
   
        
        
def savejson():
    """saves json"""
    global IMDB_SHOWS

    with open('C:/Users/josh/Documents/coding/moviesite/newdb_data/shows_asdict.txt','wb') as outfile:
        json.dump(IMDB_SHOWS, outfile)



def findguide_byzip(zipcode,headend,guidepages):
    """Goes to locatetv.com , mimicking browser and posts a zipcode and the accompanying
     value,headend, for it.  Stores cookies and reopens listings page for the values , then goes through
     each page adding the responses to a list.  Returns the list of all the pages responses."""
    totalguide=[]
    cookie_jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    urllib2.install_opener(opener)


    url_1='http://www.locatetv.com/user/region'

    values = dict(country='US', zip=zipcode, headend=headend )
    data = urllib.urlencode(values)
    request = urllib2.Request(url_1, data)

    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:18.0) Gecko/20100101 Firefox/18.0')
    request.add_header('Host', 'www.locatetv.com')
    request.add_header('Accept', 'text/html, */*; q=0.01')

    request.add_header('Connection', 'keep-alive')
    request.add_header('Referer', 'http://www.locatetv.com/listings/')
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    request.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')

    rsp = urllib2.urlopen(request)

    url_2='http://www.locatetv.com/listings/'
    request = urllib2.Request(url_2)
    rsp=urllib2.urlopen(request)
    
    totalguide.append(rsp)
   #grab cookies again

    for a in xrange(2,guidepages+1):
        print "downloading page:%s"%a
        values=dict(start="",page=str(a))
        data=urllib.urlencode(values)
        request = urllib2.Request("http://www.locatetv.com/listings/", data)
     

        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:18.0) Gecko/20100101 Firefox/18.0')
        request.add_header('Host', 'www.locatetv.com')
        request.add_header('Accept',  ' */*')
        request.add_header('Connection', 'keep-alive')
        request.add_header('Referer', 'http://www.locatetv.com/listings/')
        request.add_header('X-Requested-With', 'XMLHttpRequest')

        res  = urllib2.urlopen(request)
        totalguide.append(res)
    return totalguide


def parse_guide(totalguide,zip,headend):
    """takes a list of guides, iterates through each, then parses the data creating a list of Guide objects
    """
    global guide
    
    count=1
    for a in totalguide:
        print "Parsing page:%s"%count
        count+=1
        pageparsed = bs_parse(a.read())
        soup = BeautifulSoup(''.join(str(pageparsed)))
        shows=soup.findAll(attrs={"class":"shows"})
        channels=soup.findAll(attrs={"class":"channel"})
        channelandshow=soup.findAll(attrs={"id":"grid"})
        
        for a in range(0,len(channels)):
            channelmatch = re.search(r'name="[^"]+', str(channels[a]))
            #print channelmatch.group()
            #wholematch=re.findall(r'title="[\w\s\(\)\-\:\.\$\'\!\,\&]+',str(shows[a]))
            wholematch=re.findall(r'title="[^"]+',str(shows[a]))
            
            #titlematch=re.findall(r'title="[\w\s\(\)\:\.\$\'\!\,\&]+',str(shows[a]))
            titlematch=re.findall(r'">[^<]+</a>',str(shows[a]))
            #titlematch=re.findall(r'title="[^:]+',str(shows[a]))
            typematch=re.findall(r'<a href="/[^/]+',str(shows[a]))
    
            for a in range(0,len(titlematch)):
                timematch=re.search(r'[0-9]+:[0-9]+[a-z]+[a-z]+',wholematch[a])
                lengthmatch=re.search(r'\([0-9]+[^\)]+',wholematch[a])
                if timematch and lengthmatch: 
                    
                    #parsing the html
                    parsedtitle=parse_show_html(titlematch[a][2:-4])
                                           
                    guide.append(Guide(parsedtitle,channelmatch.group()[6:],timematch.group(),lengthmatch.group()[1:],typematch[a][10:],zip,headend))

def addguide_2db(guidelist,token):
    """checks to see if any data matches the token, if so it deletes it.  Then adds new data from guidelist to the django db
    """
    #Titles.objects.all().delete()
    Titles.objects.filter(csrftoken=token).delete()

    print "Adding titles to database"
    print len(guidelist)
    objects=[]
    for a in guidelist:
        objects.append(Titles(title=a.title, imdb_score=a.score, user_votes=a.uservotes, channel=a.channel, duration=a.length, imdb_url=a.url, time=a.time,showtype=a.showtype, zipcode=a.zipcode, headend=a.headend,csrftoken=token))
 
    Titles.objects.bulk_create(objects)
        
def parse_show_html(string):
    """parses string for html"""
    X=xmllib.XMLParser()
    try:
        parsedtitle=X.translate_references(string)
        #if string!=parsedtitle:
         #   print "parsing: %s --to-- %s"%(string,parsedtitle)
        return parsedtitle
    except:
        return string
            

def make_hash():
    """formats titles in IMDB_SHOWS so that they can be compared, then creates a hashed dictionary of IMDB_SHOWS
    """
    global IMDB_SHOWS
    showtypematch={"TV Series":'tv','TV Movie':'movie',"Mini-Series":'tv',"Movie":'movie'}
    char_tosub='[.!:;\'\ &*\(\)\-\?\,]|and|the'
    shows_hashed=dict((re.sub(char_tosub,'',d['title'].lower()),d) for d in IMDB_SHOWS)
    shows_hashedwithtype=dict((re.sub(char_tosub,'',d['title'].lower())+showtypematch[str(d['showtype'])],d) for d in IMDB_SHOWS)
    
    return shows_hashedwithtype

def check_guide(hashed):
    """takes a hashed dictionary of imdb_shows as an arg, iterates through the tv guidelist checking to see if any 
    title is in the hashed dictionary of IMDB_SHOWS, if so it adds the imdb information to the Guide instance and appends the 
    object to a list.
    """
    shows_on=[]
    for a in guide:
        title_reduced=re.sub('[.!:;\'\ &*\(\)\-\?\,]|and|the','',a.title.lower()+a.showtype)
        #print title_reduced
        if  title_reduced in hashed:
            a.url=hashed[title_reduced]['url']
            a.score=hashed[title_reduced]['imdb_score']
            a.uservotes=hashed[title_reduced]['uservotes']
            a.showtype=hashed[title_reduced]['showtype']
            shows_on.append(a)
    print "Matches in hashed guide plus re.sub:%s Titles:%s"%(len(shows_on),shows_on)
    return shows_on


def main(zip,headend,token):
    loadjson()

    totalguide=findguide_byzip(zip,headend, 12)
    parse_guide(totalguide,zip,headend)
    condense_guide()

    shows_hashed=make_hash()
    shows_on=check_guide(shows_hashed)
    addguide_2db(shows_on,token)

    
if __name__=='__main__': 
    #cProfile.run("main('19405','950','x')")
    main('19405','950','x')
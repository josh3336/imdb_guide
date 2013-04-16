 # -*- coding: utf-8 -*-
import urllib2
import re

from BeautifulSoup import BeautifulSoup        
import simplejson as json#used for storing data in json format
import jsonpickle
import xmllib#for parsing html from code to ascii
import logging

logging.basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - %(message)s')
SHOWS=[]


#Show class
class Show:
    def __init__(self,title,imdb_score,uservotes,url,year,showtype):

        self.title=title.strip()
        self.imdb_score=imdb_score
        self.uservotes=uservotes
        self.url=url
        self.year=year
        self.showtype=showtype

def loadjson():
    """loads json"""
    global SHOWS
    titles_json=[]
    logging.info("Beginning to load json")

    #loads titles
    with open('C:/Users/josh/Documents/coding/moviesite/newdb_data/shows.txt','rb') as outfile:
        titles_json=json.load(outfile)
    titles_json=titles_json["shows"]
    
   
    for a in titles_json:
        if len(a)>3:
            SHOWS.append(json.loads(a, object_hook=object_decoder))
            
def savejson_fromclass2dic():    
    """saves json"""
    global SHOWS 
    
    list_of_obj=[]
    for a in SHOWS:
        list_of_obj.append({'title':a.title,'imdb_score':a.imdb_score,'uservotes':a.uservotes,'url':a.url,'year':a.year,'showtype':a.showtype})    
    with open('C:/Users/josh/Documents/coding/moviesite/newdb_data/shows_asdict_updated.txt','wb') as outfile:
        json.dump(list_of_obj, outfile)
                    
def savejson():
    """saves json"""
    global SHOWS

    #save titles
    pickled_list=[]
    logging.info("Beginning to save json")
    for a in SHOWS:
        try:
            pickled=jsonpickle.encode(a)
            pickled_list.append(pickled)
        except:
            logging.exception("Exception: %s is not encoded properly"%a.title)
        
    obj={'shows':pickled_list}
    with open('C:/Users/josh/Documents/coding/moviesite/newdb_data/shows.txt','wb') as outfile:
        json.dump(obj, outfile)

def scrape_imdb(url,typeofshow):
    """Takes a url and adds all the entries on the page to the list of SHOWS, then goes to the next page and does the same untill 
    there is no more next pages.  If can't find a typeofshow, it adds the one listed

    """
    global SHOWS
    showslist=[]
    print url
    try:
        p=urllib2.urlopen(url)
        soup = BeautifulSoup(''.join(str(p.read())))
        lenoftitles=soup.findAll(attrs={"id":"left"})
        shows1=soup.findAll(attrs={"class":"odd detailed"})
        shows2=soup.findAll(attrs={"class":"even detailed"})
        linktonext=soup.findAll(attrs={'class':'pagination'})
        linktonextmatch=re.search(r'"/[^>]+>Next',str(linktonext))
    except:
        logging.exception("Error trying to load page %s will try again"%url)
        try:
            scrape_imdb(url,typeofshow)
        except:
            logging.exception("Error AGAIN trying to load page %s will return"%url)
        return

    #finds link to next page

    if linktonextmatch:
        linktonext=linktonextmatch.group()
        linktonext=str('http://www.imdb.com'+linktonext[1:-6])
    else: 
        logging.debug("No next link for %s"%url)
        linktonext=None  



    for a in shows1:
        showslist.append(str(a))

    for a in shows2:
        showslist.append(str(a))

    for a in showslist:
        titleyeartype=re.search(r'title="[^"]+',a)
        #finds title
        titlematch=re.search(r'[^(]+',titleyeartype.group()[7:])
        title=titlematch.group()
        title=parse_show_html(title)
        #finds year made showtype
        yearmatch=re.search(r'[0-9][0-9][0-9][0-9]',titleyeartype.group())
        showtype=typeofshow
        try:
            year=yearmatch.group()

        except:
            logging.exception("couldn't find year for %s adding none"%title)
            year=None

        urlmatch=re.search(r'<a href="[^")]+',a)
        showurl=urlmatch.group().replace('<a href="','http://www.imdb.com')
        #finds user score and votes
        scoreandvotes=re.search(r'title="Users rated[^\)]+',a)
        if scoreandvotes:
            imdb_scorematch=re.search(r'[0-9.]+',scoreandvotes.group())
            imdb_score=imdb_scorematch.group()
            imdb_votesmatch=re.search(r'\([^)]+',scoreandvotes.group())
            imdb_votes= imdb_votesmatch.group()[1:].replace(",","").split(' ')[0]
        else:
            imdb_score=None
            imdb_votes=None

        print showslist.index(a)+1
        print "Adding:%s, %s, %s, %s, %s, %s"%(title,imdb_score,imdb_votes,showurl,year,showtype)
        SHOWS.append(Show(title, imdb_score, imdb_votes,showurl,year,showtype))

    if linktonext!=None:
        logging.info("done page: %s next up: %s"%(url,linktonext))
        print url
        print linktonext
        scrape_imdb(linktonext,typeofshow)
    return

def object_decoder(obj):
    """used by json to help decode show class and store json dictionary into show class"""
    if 'py/object' in obj:
        return Show(obj['title'], obj['imdb_score'],obj['uservotes'],obj['url'],obj['year'],obj['showtype'])

def parse_show_html(string):
    """parses string for html"""
    X=xmllib.XMLParser()
    try:
        parsedtitle=X.translate_references(string)
        return parsedtitle
    except:
        return string

def scrape_movies():
    """scrapes movies from imdb
    
    """
    global SHOWS
    scrape_imdb('http://www.imdb.com/search/title?at=0&num_votes=700,&sort=user_rating&title_type=feature','Movie')

def scrape_rest():
    """scrapes rest of of content from imdb: tv series, tv movies, mini series
    
    """
    global SHOWS
    scrape_imdb('http://www.imdb.com/search/title?at=0&num_votes=300,&sort=user_rating&title_type=tv_movie','TV Movie')
    scrape_imdb('http://www.imdb.com/search/title?at=0&num_votes=300,&sort=user_rating&title_type=mini_series','Mini-Series')
    scrape_imdb('http://www.imdb.com/search/title?at=0&num_votes=75,&sort=user_rating,desc&start=1&title_type=tv_series', "TV Series")
   
def main():
    #    loadjson()
    scrape_rest()
    scrape_movies()
    savejson_fromclass2dic()


if __name__=='__main__': 
    #cProfile.run("main()")
    main()


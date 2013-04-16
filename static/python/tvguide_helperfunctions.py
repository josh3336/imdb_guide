#!/usr/bin/python
import urllib, urllib2, cookielib, re
#Working- allows you to change the zip code posts the form and gets back the form data with the desired zip code



def return_providers(zipcode):
    """takes a zip code and uses locatetv, to return a dictionary mapping service provider to headend value for that zipcode"""
    
    cookie_jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    urllib2.install_opener(opener)

    # acquire cookie
    url_1='http://www.locatetv.com/user/region'

    values = dict(country='US', zip=zipcode)
    data = urllib.urlencode(values)
    request = urllib2.Request(url_1, data)

    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:18.0) Gecko/20100101 Firefox/18.0')
    request.add_header('Host', 'www.locatetv.com')
    request.add_header('Accept', 'text/html, */*; q=0.01')
    request.add_header('Connection', 'keep-alive')
    request.add_header('Referer', 'http://www.locatetv.com/listings/')
    request.add_header('X-Requested-With', 'XMLHttpRequest')
    request.add_header('Content-Length','20')
    request.add_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')

    rsp = urllib2.urlopen(request)
    content = rsp.read()

    tvproviders=re.search(r'TV Service Provider[\s\S\w\W]+',content)
    tvproviders=str(tvproviders.group())
    providers_list=re.findall(r'option value=[^<]+',tvproviders)

    provider_value={}

    for a in providers_list:
        provider=re.search(r'>[\s\S\w\W]+',a)
        value=re.search(r'value="[^"]+',a)
        provider_value[provider.group()[1:]]=value.group()[7:]
    return provider_value




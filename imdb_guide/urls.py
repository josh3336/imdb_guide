from django.conf.urls import patterns, include, url
from imdb_guide.views import home, entered, contact, about, findproviders
from titles.views import guide, guide_filtered, ondemand
from dajaxice.core import dajaxice_autodiscover
from django.views.static import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#use next two lines for dajax
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'imdb_guide.views.home', name='home'),
    # url(r'^imdb_guide/', include('imdb_guide.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
            (r'home/$',home),
            (r'^allguide/$',guide),
            (r'^guide/$',guide_filtered),
            (r'^contact/$',contact),
            (r'^about/$',about),
            (r'^entered/$', entered),
            (r'^ondemand/$', ondemand),
            (r'[\w\W]+findproviders.html/$', findproviders),
            url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
            (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
            (r'^mymedia/(?P<path>.*)$', 'django.views.static.serve',  
            {'document_root':     settings.MEDIA_ROOT}),
            )



urlpatterns += staticfiles_urlpatterns()
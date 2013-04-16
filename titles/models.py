from django.db import models
from datetime import datetime
# Create your models here.

class Titles(models.Model):
    title = models.CharField(max_length=50)
    imdb_score = models.FloatField(max_length=60)
    user_votes = models.IntegerField(max_length=30)
    channel = models.CharField(max_length=50)
    duration=models.CharField(max_length=50)
    time=models.TimeField(auto_now=False, auto_now_add=False)
    showtype=models.CharField(max_length=50,null=True, blank=True)
    imdb_url = models.URLField()
    zipcode = models.CharField(max_length=10)
    headend = models.CharField(max_length=10)
    #year=models.IntegerField(max_length=30)
    time_entered=models.DateTimeField(default=datetime.now(), editable='False',null=True)
    csrftoken = models.CharField(max_length=50)
    def __unicode__(self):
        return u'%s, %s, %s, %s, %s, %s, %s' % (self.title, self.imdb_score, self.user_votes, self.channel, self.duration, self.time, self.imdb_url)


class Ondemand_Titles(models.Model):
    title = models.CharField(max_length=50)
    imdb_score = models.FloatField(max_length=60)
    user_votes = models.IntegerField(max_length=30)
    channel = models.CharField(max_length=50)
    showtype=models.CharField(max_length=50,null=True, blank=True)
    imdb_url = models.URLField()
    time_entered=models.DateTimeField(default=datetime.now(), editable='False',null=True)
    def __unicode__(self):
        return u'%s, %s, %s, %s, %s, %s, %s' % (self.title, self.imdb_score, self.user_votes, self.channel,self.imdb_url)


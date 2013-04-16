#tables.py
import django_tables2 as tables
from titles.models import Titles, Ondemand_Titles
from django.utils.safestring import mark_safe

class TitlesTable(tables.Table):
    def render_title(self, value, record):
        return mark_safe('''<a href=%s target="_blank">%s</a>''' % (record.imdb_url, value))


    class Meta:
        model = Titles
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("title","imdb_score", "user_votes","channel","duration","time","showtype")
        template="django_tables2/tablewithcolor.html"
        order_by="-imdb_score"


class TestTable(tables.Table):
    def render_title(self, value, record):
        return mark_safe('''<a href=%s target="_blank">%s</a>''' % (record.imdb_url, value))

    class Meta:
        model = Titles
        attrs = {"class": "paleblue"}



class OndemandTable(tables.Table):
    def render_title(self, value, record):
        return mark_safe('''<a href=%s target="_blank">%s</a>''' % (record.imdb_url, value))


    class Meta:
        model = Titles
        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
        fields = ("title","imdb_score", "user_votes","channel","showtype")
        template="django_tables2/tablewithcolor.html"
        order_by="-imdb_score"

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Titles.year'
        db.delete_column('titles_titles', 'year')


    def backwards(self, orm):
        # Adding field 'Titles.year'
        db.add_column('titles_titles', 'year',
                      self.gf('django.db.models.fields.IntegerField')(default=1, max_length=30),
                      keep_default=False)


    models = {
        'titles.titles': {
            'Meta': {'object_name': 'Titles'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'headend': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_score': ('django.db.models.fields.FloatField', [], {'max_length': '60'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'showtype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'time_entered': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_votes': ('django.db.models.fields.IntegerField', [], {'max_length': '30'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['titles']
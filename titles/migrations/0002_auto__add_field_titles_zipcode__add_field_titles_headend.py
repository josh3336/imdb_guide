# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Titles.zipcode'
        db.add_column('titles_titles', 'zipcode',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=10),
                      keep_default=False)

        # Adding field 'Titles.headend'
        db.add_column('titles_titles', 'headend',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Titles.zipcode'
        db.delete_column('titles_titles', 'zipcode')

        # Deleting field 'Titles.headend'
        db.delete_column('titles_titles', 'headend')


    models = {
        'titles.titles': {
            'Meta': {'object_name': 'Titles'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'headend': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_score': ('django.db.models.fields.FloatField', [], {'max_length': '60'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'showtype': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_votes': ('django.db.models.fields.IntegerField', [], {'max_length': '30'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['titles']
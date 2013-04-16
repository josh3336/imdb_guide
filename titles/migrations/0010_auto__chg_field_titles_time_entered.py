# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Titles.time_entered'
        db.alter_column('titles_titles', 'time_entered', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'Titles.time_entered'
        db.alter_column('titles_titles', 'time_entered', self.gf('django.db.models.fields.DateTimeField')())

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
            'time_entered': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 3, 6, 0, 0)', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_votes': ('django.db.models.fields.IntegerField', [], {'max_length': '30'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['titles']
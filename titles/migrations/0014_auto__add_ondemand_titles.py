# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ondemand_Titles'
        db.create_table('titles_ondemand_titles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('imdb_score', self.gf('django.db.models.fields.FloatField')(max_length=60)),
            ('user_votes', self.gf('django.db.models.fields.IntegerField')(max_length=30)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('showtype', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('imdb_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('time_entered', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 5, 0, 0), null=True)),
        ))
        db.send_create_signal('titles', ['Ondemand_Titles'])


    def backwards(self, orm):
        # Deleting model 'Ondemand_Titles'
        db.delete_table('titles_ondemand_titles')


    models = {
        'titles.ondemand_titles': {
            'Meta': {'object_name': 'Ondemand_Titles'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_score': ('django.db.models.fields.FloatField', [], {'max_length': '60'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'showtype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'time_entered': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 5, 0, 0)', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_votes': ('django.db.models.fields.IntegerField', [], {'max_length': '30'})
        },
        'titles.titles': {
            'Meta': {'object_name': 'Titles'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'csrftoken': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'headend': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_score': ('django.db.models.fields.FloatField', [], {'max_length': '60'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'showtype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'time_entered': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 5, 0, 0)', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_votes': ('django.db.models.fields.IntegerField', [], {'max_length': '30'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['titles']
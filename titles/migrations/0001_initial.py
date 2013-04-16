# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Titles'
        db.create_table('titles_titles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('imdb_score', self.gf('django.db.models.fields.FloatField')(max_length=60)),
            ('user_votes', self.gf('django.db.models.fields.IntegerField')(max_length=30)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('duration', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('time', self.gf('django.db.models.fields.TimeField')()),
            ('showtype', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('imdb_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('titles', ['Titles'])


    def backwards(self, orm):
        # Deleting model 'Titles'
        db.delete_table('titles_titles')


    models = {
        'titles.titles': {
            'Meta': {'object_name': 'Titles'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_score': ('django.db.models.fields.FloatField', [], {'max_length': '60'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'showtype': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.TimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_votes': ('django.db.models.fields.IntegerField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['titles']
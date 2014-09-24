# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'New'
        db.create_table(u'apps_new', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('header', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'apps', ['New'])


    def backwards(self, orm):
        # Deleting model 'New'
        db.delete_table(u'apps_new')


    models = {
        u'apps.new': {
            'Meta': {'object_name': 'New'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['apps']
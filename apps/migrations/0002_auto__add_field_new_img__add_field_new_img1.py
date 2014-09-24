# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'New.img'
        db.add_column(u'apps_new', 'img',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1024, blank=True),
                      keep_default=False)

        # Adding field 'New.img1'
        db.add_column(u'apps_new', 'img1',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'New.img'
        db.delete_column(u'apps_new', 'img')

        # Deleting field 'New.img1'
        db.delete_column(u'apps_new', 'img1')


    models = {
        u'apps.new': {
            'Meta': {'object_name': 'New'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'blank': 'True'}),
            'img1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['apps']
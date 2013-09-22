# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TempSeries'
        db.create_table(u'piweb_tempseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'piweb', ['TempSeries'])

        # Adding model 'TempReading'
        db.create_table(u'piweb_tempreading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tempseries', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['piweb.TempSeries'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('scale', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'piweb', ['TempReading'])

        # Adding unique constraint on 'TempReading', fields ['tempseries', 'timestamp']
        db.create_unique(u'piweb_tempreading', ['tempseries_id', 'timestamp'])


    def backwards(self, orm):
        # Removing unique constraint on 'TempReading', fields ['tempseries', 'timestamp']
        db.delete_unique(u'piweb_tempreading', ['tempseries_id', 'timestamp'])

        # Deleting model 'TempSeries'
        db.delete_table(u'piweb_tempseries')

        # Deleting model 'TempReading'
        db.delete_table(u'piweb_tempreading')


    models = {
        u'piweb.tempreading': {
            'Meta': {'unique_together': "(('tempseries', 'timestamp'),)", 'object_name': 'TempReading'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scale': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'tempseries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['piweb.TempSeries']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'piweb.tempseries': {
            'Meta': {'object_name': 'TempSeries'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['piweb']
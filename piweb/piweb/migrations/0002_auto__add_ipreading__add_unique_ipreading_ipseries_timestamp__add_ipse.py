# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IPReading'
        db.create_table(u'piweb_ipreading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ipseries', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['piweb.IPSeries'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
        ))
        db.send_create_signal(u'piweb', ['IPReading'])

        # Adding unique constraint on 'IPReading', fields ['ipseries', 'timestamp']
        db.create_unique(u'piweb_ipreading', ['ipseries_id', 'timestamp'])

        # Adding model 'IPSeries'
        db.create_table(u'piweb_ipseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'piweb', ['IPSeries'])


    def backwards(self, orm):
        # Removing unique constraint on 'IPReading', fields ['ipseries', 'timestamp']
        db.delete_unique(u'piweb_ipreading', ['ipseries_id', 'timestamp'])

        # Deleting model 'IPReading'
        db.delete_table(u'piweb_ipreading')

        # Deleting model 'IPSeries'
        db.delete_table(u'piweb_ipseries')


    models = {
        u'piweb.ipreading': {
            'Meta': {'unique_together': "(('ipseries', 'timestamp'),)", 'object_name': 'IPReading'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipseries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['piweb.IPSeries']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'value': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'piweb.ipseries': {
            'Meta': {'object_name': 'IPSeries'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
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
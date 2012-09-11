# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PendingLocation'
        db.delete_table('map_pendinglocation')


    def backwards(self, orm):
        # Adding model 'PendingLocation'
        db.create_table('map_pendinglocation', (
            ('location_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['map.Location'], unique=True, primary_key=True)),
            ('existing', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', null=True, to=orm['map.Location'], blank=True)),
        ))
        db.send_create_signal('map', ['PendingLocation'])


    models = {
        'map.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fix_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hiring': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'permalink': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['map.Type']", 'symmetrical': 'False'})
        },
        'map.type': {
            'Meta': {'ordering': "['name']", 'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['map.Type']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['map']
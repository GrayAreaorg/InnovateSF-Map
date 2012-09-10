# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table('map_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('permalink', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('fix_address', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('map', ['Location'])

        # Adding M2M table for field type on 'Location'
        db.create_table('map_location_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('location', models.ForeignKey(orm['map.location'], null=False)),
            ('type', models.ForeignKey(orm['map.type'], null=False))
        ))
        db.create_unique('map_location_type', ['location_id', 'type_id'])

        # Adding model 'Type'
        db.create_table('map_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['map.Type'], null=True, blank=True)),
        ))
        db.send_create_signal('map', ['Type'])


    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table('map_location')

        # Removing M2M table for field type on 'Location'
        db.delete_table('map_location_type')

        # Deleting model 'Type'
        db.delete_table('map_type')


    models = {
        'map.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fix_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'permalink': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['map.Type']", 'symmetrical': 'False'})
        },
        'map.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['map.Type']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['map']
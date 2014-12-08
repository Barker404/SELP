# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Attack'
        db.create_table(u'mechs_attack', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('damage', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'mechs', ['Attack'])

        # Adding model 'StdMech'
        db.create_table(u'mechs_stdmech', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('attackA', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attackA', to=orm['mechs.Attack'])),
            ('attackB', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attackB', blank=True, to=orm['mechs.Attack'])),
            ('attackC', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attackC', blank=True, to=orm['mechs.Attack'])),
        ))
        db.send_create_signal(u'mechs', ['StdMech'])


    def backwards(self, orm):
        # Deleting model 'Attack'
        db.delete_table(u'mechs_attack')

        # Deleting model 'StdMech'
        db.delete_table(u'mechs_stdmech')


    models = {
        u'mechs.attack': {
            'Meta': {'object_name': 'Attack'},
            'damage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'mechs.stdmech': {
            'Meta': {'object_name': 'StdMech'},
            'attackA': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attackA'", 'to': u"orm['mechs.Attack']"}),
            'attackB': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attackB'", 'blank': 'True', 'to': u"orm['mechs.Attack']"}),
            'attackC': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attackC'", 'blank': 'True', 'to': u"orm['mechs.Attack']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['mechs']
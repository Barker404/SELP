# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Battle.distance'
        db.add_column(u'battles_battle', 'distance',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Battle.distance'
        db.delete_column(u'battles_battle', 'distance')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'battles.battle': {
            'Meta': {'object_name': 'Battle'},
            'distance': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastMoveTime': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'player1': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'related_name': "'player1'", 'unique': 'True', 'null': 'True', 'to': u"orm['battles.Player']"}),
            'player2': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'related_name': "'player2'", 'unique': 'True', 'null': 'True', 'to': u"orm['battles.Player']"}),
            'startTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'turnNumber': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'winner'", 'null': 'True', 'to': u"orm['battles.Player']"})
        },
        u'battles.move': {
            'Meta': {'object_name': 'Move'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moveNo': ('django.db.models.fields.IntegerField', [], {}),
            'moveUsed': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['battles.Player']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'battles.player': {
            'Meta': {'object_name': 'Player'},
            'currentMove': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'currentMove'", 'null': 'True', 'to': u"orm['battles.Move']"}),
            'hp': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastMove': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'lastMove'", 'null': 'True', 'to': u"orm['battles.Move']"}),
            'opponent': ('django.db.models.fields.related.OneToOneField', [], {'default': 'None', 'related_name': "'_opponent'", 'unique': 'True', 'null': 'True', 'to': u"orm['battles.Player']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['battles']
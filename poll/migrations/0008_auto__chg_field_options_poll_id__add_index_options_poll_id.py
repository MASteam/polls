# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Options.poll_id' to match new field type.
        db.rename_column(u'poll_options', 'poll_id', 'poll_id_id')
        # Changing field 'Options.poll_id'
        db.alter_column(u'poll_options', 'poll_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Polls']))
        # Adding index on 'Options', fields ['poll_id']
        db.create_index(u'poll_options', ['poll_id_id'])


    def backwards(self, orm):
        # Removing index on 'Options', fields ['poll_id']
        db.delete_index(u'poll_options', ['poll_id_id'])


        # Renaming column for 'Options.poll_id' to match new field type.
        db.rename_column(u'poll_options', 'poll_id_id', 'poll_id')
        # Changing field 'Options.poll_id'
        db.alter_column(u'poll_options', 'poll_id', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'poll.comments': {
            'Meta': {'object_name': 'Comments'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'poll_id': ('django.db.models.fields.IntegerField', [], {}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 19, 0, 0)', 'null': 'True'}),
            'user_ip': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'poll.options': {
            'Meta': {'object_name': 'Options'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'poll_id': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['poll.Polls']"})
        },
        u'poll.optionsvotes': {
            'Meta': {'object_name': 'OptionsVotes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll_id': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 19, 0, 0)', 'null': 'True'}),
            'user_ip': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'vote_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'poll.polls': {
            'Meta': {'object_name': 'Polls'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 19, 0, 0)', 'null': 'True'})
        }
    }

    complete_apps = ['poll']
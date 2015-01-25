# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OptionsVotes.time'
        db.alter_column(u'poll_optionsvotes', 'time', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Polls.time'
        db.alter_column(u'poll_polls', 'time', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # Changing field 'OptionsVotes.time'
        db.alter_column(u'poll_optionsvotes', 'time', self.gf('django.db.models.fields.DateTimeField')(default=0))

        # Changing field 'Polls.time'
        db.alter_column(u'poll_polls', 'time', self.gf('django.db.models.fields.DateTimeField')(default=1))

    models = {
        u'poll.options': {
            'Meta': {'object_name': 'Options'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'poll_id': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'poll.optionsvotes': {
            'Meta': {'object_name': 'OptionsVotes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll_id': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user_ip': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'vote_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'poll.polls': {
            'Meta': {'object_name': 'Polls'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['poll']
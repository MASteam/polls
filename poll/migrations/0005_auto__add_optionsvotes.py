# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OptionsVotes'
        db.create_table(u'poll_optionsvotes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll_id', self.gf('django.db.models.fields.IntegerField')()),
            ('vote_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_ip', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'poll', ['OptionsVotes'])


    def backwards(self, orm):
        # Deleting model 'OptionsVotes'
        db.delete_table(u'poll_optionsvotes')


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
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'user_ip': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'vote_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'poll.polls': {
            'Meta': {'object_name': 'Polls'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['poll']
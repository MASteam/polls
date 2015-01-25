# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Polls'
        db.create_table(u'poll_polls', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 18, 0, 0))),
        ))
        db.send_create_signal(u'poll', ['Polls'])


    def backwards(self, orm):
        # Deleting model 'Polls'
        db.delete_table(u'poll_polls')


    models = {
        u'poll.polls': {
            'Meta': {'object_name': 'Polls'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 18, 0, 0)'})
        }
    }

    complete_apps = ['poll']
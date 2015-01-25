# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'OptionsVotes.poll_id'
        db.delete_column(u'poll_optionsvotes', 'poll_id')

        # Adding field 'OptionsVotes.poll'
        db.add_column(u'poll_optionsvotes', 'poll',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Polls'], null=True),
                      keep_default=False)

        # Deleting field 'Comments.poll_id'
        db.delete_column(u'poll_comments', 'poll_id')

        # Adding field 'Comments.poll'
        db.add_column(u'poll_comments', 'poll',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Polls'], null=True),
                      keep_default=False)


        # Changing field 'Options.poll'
        db.alter_column(u'poll_options', 'poll_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Polls'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'OptionsVotes.poll_id'
        raise RuntimeError("Cannot reverse this migration. 'OptionsVotes.poll_id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'OptionsVotes.poll_id'
        db.add_column(u'poll_optionsvotes', 'poll_id',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)

        # Deleting field 'OptionsVotes.poll'
        db.delete_column(u'poll_optionsvotes', 'poll_id')


        # User chose to not deal with backwards NULL issues for 'Comments.poll_id'
        raise RuntimeError("Cannot reverse this migration. 'Comments.poll_id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Comments.poll_id'
        db.add_column(u'poll_comments', 'poll_id',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)

        # Deleting field 'Comments.poll'
        db.delete_column(u'poll_comments', 'poll_id')


        # Changing field 'Options.poll'
        db.alter_column(u'poll_options', 'poll_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['poll.Polls']))

    models = {
        u'poll.comments': {
            'Meta': {'object_name': 'Comments'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['poll.Polls']", 'null': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 19, 0, 0)', 'null': 'True'}),
            'user_ip': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'poll.options': {
            'Meta': {'object_name': 'Options'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['poll.Polls']", 'null': 'True'})
        },
        u'poll.optionsvotes': {
            'Meta': {'object_name': 'OptionsVotes'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['poll.Polls']", 'null': 'True'}),
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
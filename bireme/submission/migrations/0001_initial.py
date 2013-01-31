# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Step'
        db.create_table('submission_step', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.Type'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.Step'], null=True, blank=True)),
            ('finish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pending', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('close', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_edit', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('submission', ['Step'])

        # Adding model 'StepLocal'
        db.create_table('submission_steplocal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('step', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.Step'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='pt-br', max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('submission', ['StepLocal'])

        # Adding model 'LildbiVersion'
        db.create_table('submission_lildbiversion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('submission', ['LildbiVersion'])

        # Adding model 'Type'
        db.create_table('submission_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('submission', ['Type'])

        # Adding model 'BibliographicType'
        db.create_table('submission_bibliographictype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('submission', ['BibliographicType'])

        # Adding model 'BibliographicTypeLocal'
        db.create_table('submission_bibliographictypelocal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('bibliographic_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.BibliographicType'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='pt-br', max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('submission', ['BibliographicTypeLocal'])

        # Adding model 'TypeSubmission'
        db.create_table('submission_typesubmission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.Submission'], unique=True)),
            ('bibliographic_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.BibliographicType'], null=True)),
            ('total_records', self.gf('django.db.models.fields.CharField')(default=0, max_length=255, null=True, blank=True)),
            ('certified', self.gf('django.db.models.fields.CharField')(default=0, max_length=255, null=True, blank=True)),
            ('iso_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('lildbi_version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.LildbiVersion'], null=True, blank=True)),
        ))
        db.send_create_signal('submission', ['TypeSubmission'])

        # Adding model 'Submission'
        db.create_table('submission_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.Type'])),
            ('current_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.Step'])),
            ('observation', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('submission', ['Submission'])

        # Adding model 'FollowUp'
        db.create_table('submission_followup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625244))),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 31, 17, 29, 53, 625290))),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('updater', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submission.Submission'])),
            ('previous_status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['submission.Step'])),
            ('current_status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['submission.Step'])),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('staff_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('submission', ['FollowUp'])


    def backwards(self, orm):
        
        # Deleting model 'Step'
        db.delete_table('submission_step')

        # Deleting model 'StepLocal'
        db.delete_table('submission_steplocal')

        # Deleting model 'LildbiVersion'
        db.delete_table('submission_lildbiversion')

        # Deleting model 'Type'
        db.delete_table('submission_type')

        # Deleting model 'BibliographicType'
        db.delete_table('submission_bibliographictype')

        # Deleting model 'BibliographicTypeLocal'
        db.delete_table('submission_bibliographictypelocal')

        # Deleting model 'TypeSubmission'
        db.delete_table('submission_typesubmission')

        # Deleting model 'Submission'
        db.delete_table('submission_submission')

        # Deleting model 'FollowUp'
        db.delete_table('submission_followup')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'submission.bibliographictype': {
            'Meta': {'object_name': 'BibliographicType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'submission.bibliographictypelocal': {
            'Meta': {'object_name': 'BibliographicTypeLocal'},
            'bibliographic_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.BibliographicType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'pt-br'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'submission.followup': {
            'Meta': {'object_name': 'FollowUp'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'current_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['submission.Step']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'previous_status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['submission.Step']"}),
            'staff_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.Submission']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'submission.lildbiversion': {
            'Meta': {'object_name': 'LildbiVersion'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'submission.step': {
            'Meta': {'object_name': 'Step'},
            'allow_edit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'close': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'finish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.Step']", 'null': 'True', 'blank': 'True'}),
            'pending': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.Type']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'submission.steplocal': {
            'Meta': {'object_name': 'StepLocal'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'pt-br'", 'max_length': '255'}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.Step']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'submission.submission': {
            'Meta': {'object_name': 'Submission'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'current_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.Step']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.Type']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'submission.type': {
            'Meta': {'object_name': 'Type'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'submission.typesubmission': {
            'Meta': {'object_name': 'TypeSubmission'},
            'bibliographic_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.BibliographicType']", 'null': 'True'}),
            'certified': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625244)'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'lildbi_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.LildbiVersion']", 'null': 'True', 'blank': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submission.Submission']", 'unique': 'True'}),
            'total_records': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 31, 17, 29, 53, 625290)'}),
            'updater': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['submission']

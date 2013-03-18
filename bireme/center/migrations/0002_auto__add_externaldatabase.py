# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExternalDatabase'
        db.create_table('center_externaldatabase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('center', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['center.Center'], null=True, blank=True)),
        ))
        db.send_create_signal('center', ['ExternalDatabase'])


    def backwards(self, orm):
        
        # Deleting model 'ExternalDatabase'
        db.delete_table('center_externaldatabase')


    models = {
        'center.center': {
            'Meta': {'object_name': 'Center'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'center.externaldatabase': {
            'Meta': {'object_name': 'ExternalDatabase'},
            'center': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['center.Center']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['center']

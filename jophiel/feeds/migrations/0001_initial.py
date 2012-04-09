# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Feed'
        db.create_table('feeds_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('orig_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('url_etag', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('url_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url_status', self.gf('django.db.models.fields.CharField')(default='200', max_length=100)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.TextField')(default='')),
            ('author', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('article_num', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('feeds', ['Feed'])

        # Adding model 'FeedMeta'
        db.create_table('feeds_feedmeta', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('title', self.gf('django.db.models.fields.TextField')(default='')),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('tagline', self.gf('django.db.models.fields.TextField')(default='')),
            ('info', self.gf('django.db.models.fields.TextField')(default='')),
            ('author', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('publisher', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('generator', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('category', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('copyright', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('license', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('docs', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('errorreportsto', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image_title', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('image_width', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image_height', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('feed', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['feeds.Feed'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('feeds', ['FeedMeta'])

        # Adding model 'Planet'
        db.create_table('feeds_planet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('owner_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('owner_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('owner_email', self.gf('django.db.models.fields.EmailField')(max_length=255, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('feeds', ['Planet'])

        # Adding M2M table for field feeds on 'Planet'
        db.create_table('feeds_planet_feeds', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('planet', models.ForeignKey(orm['feeds.planet'], null=False)),
            ('feed', models.ForeignKey(orm['feeds.feed'], null=False))
        ))
        db.create_unique('feeds_planet_feeds', ['planet_id', 'feed_id'])

        # Adding model 'Article'
        db.create_table('feeds_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('id_hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('publish', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('hidden', self.gf('django.db.models.fields.CharField')(default=False, max_length=255)),
            ('isexpired', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('summary', self.gf('django.db.models.fields.TextField')(default='')),
            ('content', self.gf('django.db.models.fields.TextField')(default='')),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('issued', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('expired', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('source_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['feeds.Feed'])),
        ))
        db.send_create_signal('feeds', ['Article'])


    def backwards(self, orm):
        
        # Deleting model 'Feed'
        db.delete_table('feeds_feed')

        # Deleting model 'FeedMeta'
        db.delete_table('feeds_feedmeta')

        # Deleting model 'Planet'
        db.delete_table('feeds_planet')

        # Removing M2M table for field feeds on 'Planet'
        db.delete_table('feeds_planet_feeds')

        # Deleting model 'Article'
        db.delete_table('feeds_article')


    models = {
        'feeds.article': {
            'Meta': {'ordering': "('publish', 'title')", 'object_name': 'Article'},
            'article_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'expired': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['feeds.Feed']"}),
            'hidden': ('django.db.models.fields.CharField', [], {'default': 'False', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'isexpired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'issued': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'publish': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'source_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'source_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'feeds.feed': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Feed'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'article_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'image_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'orig_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'url_etag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'url_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'url_status': ('django.db.models.fields.CharField', [], {'default': "'200'", 'max_length': '100'})
        },
        'feeds.feedmeta': {
            'Meta': {'object_name': 'FeedMeta'},
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'copyright': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'docs': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'errorreportsto': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'feed': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feeds.Feed']", 'unique': 'True', 'primary_key': 'True'}),
            'generator': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'image_height': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'image_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'image_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'image_width': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'info': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'license': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'tagline': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'title': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'feeds.planet': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Planet'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['feeds.Feed']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'owner_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'owner_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['feeds']

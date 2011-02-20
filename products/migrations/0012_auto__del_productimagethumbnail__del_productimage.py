# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ProductImageThumbnail'
        db.delete_table('products_productimagethumbnail')

        # Deleting model 'ProductImage'
        db.delete_table('products_productimage')


    def backwards(self, orm):
        
        # Adding model 'ProductImageThumbnail'
        db.create_table('products_productimagethumbnail', (
            ('main_image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.ProductImage'], unique=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('img_height', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('img_width', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('products', ['ProductImageThumbnail'])

        # Adding model 'ProductImage'
        db.create_table('products_productimage', (
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Product'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('img_height', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('img_width', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('products', ['ProductImage'])


    models = {
        'products.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'products.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('dropship.products.fields.CurrencyField', [], {'max_digits': '19', 'decimal_places': '2'}),
            'stock': ('django.db.models.fields.BigIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['products']

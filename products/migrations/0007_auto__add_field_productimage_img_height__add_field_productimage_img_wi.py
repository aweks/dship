# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'ProductImage.img_height'
        db.add_column('products_productimage', 'img_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'ProductImage.img_width'
        db.add_column('products_productimage', 'img_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Changing field 'ProductImage.caption'
        db.alter_column('products_productimage', 'caption', self.gf('django.db.models.fields.CharField')(max_length=512, null=True))


    def backwards(self, orm):
        
        # Deleting field 'ProductImage.img_height'
        db.delete_column('products_productimage', 'img_height')

        # Deleting field 'ProductImage.img_width'
        db.delete_column('products_productimage', 'img_width')

        # Changing field 'ProductImage.caption'
        db.alter_column('products_productimage', 'caption', self.gf('django.db.models.fields.CharField')(default=0, max_length=512))


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
        },
        'products.productimage': {
            'Meta': {'object_name': 'ProductImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'img_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['products']

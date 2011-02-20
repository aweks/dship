# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ProductImage.img_width'
        db.alter_column('products_productimage', 'img_width', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Changing field 'ProductImage.img_height'
        db.alter_column('products_productimage', 'img_height', self.gf('django.db.models.fields.PositiveIntegerField')())


    def backwards(self, orm):
        
        # Changing field 'ProductImage.img_width'
        db.alter_column('products_productimage', 'img_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

        # Changing field 'ProductImage.img_height'
        db.alter_column('products_productimage', 'img_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')())


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
            'img_height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'img_width': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['products']

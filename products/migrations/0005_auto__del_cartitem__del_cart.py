# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'CartItem'
        db.delete_table('products_cartitem')

        # Deleting model 'Cart'
        db.delete_table('products_cart')


    def backwards(self, orm):
        
        # Adding model 'CartItem'
        db.create_table('products_cartitem', (
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Cart'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Product'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['order.ShippingAddress'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('products', ['CartItem'])

        # Adding model 'Cart'
        db.create_table('products_cart', (
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('products', ['Cart'])


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

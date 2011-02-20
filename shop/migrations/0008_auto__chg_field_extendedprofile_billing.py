# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ExtendedProfile.billing'
        db.alter_column('shop_extendedprofile', 'billing_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.BillingAddress'], null=True))


    def backwards(self, orm):
        
        # Changing field 'ExtendedProfile.billing'
        db.alter_column('shop_extendedprofile', 'billing_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['shop.BillingAddress']))


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
        'shop.billingaddress': {
            'Meta': {'object_name': 'BillingAddress'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'addressee': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'shop.cart': {
            'Meta': {'object_name': 'Cart'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total': ('dropship.products.fields.CurrencyField', [], {'max_digits': '19', 'decimal_places': '2'})
        },
        'shop.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.ShippingAddress']"}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'other_cost': ('dropship.products.fields.CurrencyField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.BigIntegerField', [], {}),
            'total': ('dropship.products.fields.CurrencyField', [], {'max_digits': '19', 'decimal_places': '2'})
        },
        'shop.extendedprofile': {
            'Meta': {'object_name': 'ExtendedProfile'},
            'billing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.BillingAddress']", 'null': 'True', 'blank': 'True'}),
            'commission_rate': ('dropship.products.fields.CurrencyField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'shop.order': {
            'Meta': {'object_name': 'Order'},
            'billing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.BillingAddress']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'total': ('dropship.products.fields.CurrencyField', [], {'max_digits': '19', 'decimal_places': '2'})
        },
        'shop.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.ShippingAddress']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Product']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Order']"}),
            'other_cost': ('dropship.products.fields.CurrencyField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '2', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.BigIntegerField', [], {}),
            'total': ('dropship.products.fields.CurrencyField', [], {'max_digits': '19', 'decimal_places': '2'})
        },
        'shop.shippingaddress': {
            'Meta': {'object_name': 'ShippingAddress'},
            'address_one': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'address_two': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'addressee': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['shop']

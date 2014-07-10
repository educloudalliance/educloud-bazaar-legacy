# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'catalogue_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('numchild', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'catalogue', ['Category'])

        # Adding model 'ProductClass'
        db.create_table(u'catalogue_productclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('oscar.models.fields.autoslugfield.AutoSlugField')(allow_duplicates=False, max_length=128, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
            ('requires_shipping', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('track_stock', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductClass'])

        # Adding M2M table for field options on 'ProductClass'
        m2m_table_name = db.shorten_name(u'catalogue_productclass_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productclass', models.ForeignKey(orm[u'catalogue.productclass'], null=False)),
            ('option', models.ForeignKey(orm[u'catalogue.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['productclass_id', 'option_id'])

        # Adding model 'ProductCategory'
        db.create_table(u'catalogue_productcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Product'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Category'])),
        ))
        db.send_create_signal(u'catalogue', ['ProductCategory'])

        # Adding unique constraint on 'ProductCategory', fields ['product', 'category']
        db.create_unique(u'catalogue_productcategory', ['product_id', 'category_id'])

        # Adding model 'Product'
        db.create_table(u'catalogue_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upc', self.gf('oscar.models.fields.NullCharField')(max_length=64, unique=True, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='variants', null=True, to=orm['catalogue.Product'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('product_class', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', null=True, on_delete=models.PROTECT, to=orm['catalogue.ProductClass'])),
            ('rating', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, db_index=True, blank=True)),
            ('is_discountable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'catalogue', ['Product'])

        # Adding M2M table for field product_options on 'Product'
        m2m_table_name = db.shorten_name(u'catalogue_product_product_options')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm[u'catalogue.product'], null=False)),
            ('option', models.ForeignKey(orm[u'catalogue.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['product_id', 'option_id'])

        # Adding model 'ProductAttribute'
        db.create_table(u'catalogue_productattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_class', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='attributes', null=True, to=orm['catalogue.ProductClass'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('django.db.models.fields.SlugField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(default='text', max_length=20)),
            ('option_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AttributeOptionGroup'], null=True, blank=True)),
            ('entity_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AttributeEntityType'], null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'catalogue', ['ProductAttribute'])

        # Adding model 'ProductAttributeValue'
        db.create_table(u'catalogue_productattributevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.ProductAttribute'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attribute_values', to=orm['catalogue.Product'])),
            ('value_text', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('value_integer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('value_boolean', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('value_float', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('value_richtext', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('value_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('value_option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AttributeOption'], null=True, blank=True)),
            ('value_entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.AttributeEntity'], null=True, blank=True)),
            ('value_file', self.gf('django.db.models.fields.files.FileField')(max_length=255, null=True, blank=True)),
            ('value_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductAttributeValue'])

        # Adding unique constraint on 'ProductAttributeValue', fields ['attribute', 'product']
        db.create_unique(u'catalogue_productattributevalue', ['attribute_id', 'product_id'])

        # Adding model 'AttributeOptionGroup'
        db.create_table(u'catalogue_attributeoptiongroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'catalogue', ['AttributeOptionGroup'])

        # Adding model 'AttributeOption'
        db.create_table(u'catalogue_attributeoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', to=orm['catalogue.AttributeOptionGroup'])),
            ('option', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'catalogue', ['AttributeOption'])

        # Adding model 'AttributeEntity'
        db.create_table(u'catalogue_attributeentity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entities', to=orm['catalogue.AttributeEntityType'])),
        ))
        db.send_create_signal(u'catalogue', ['AttributeEntity'])

        # Adding model 'AttributeEntityType'
        db.create_table(u'catalogue_attributeentitytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['AttributeEntityType'])

        # Adding model 'Option'
        db.create_table(u'catalogue_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('code', self.gf('oscar.models.fields.autoslugfield.AutoSlugField')(allow_duplicates=False, max_length=128, separator=u'-', blank=True, unique=True, populate_from='name', overwrite=False)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Required', max_length=128)),
        ))
        db.send_create_signal(u'catalogue', ['Option'])

        # Adding model 'ProductImage'
        db.create_table(u'catalogue_productimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['catalogue.Product'])),
            ('original', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('display_order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductImage'])

        # Adding unique constraint on 'ProductImage', fields ['product', 'display_order']
        db.create_unique(u'catalogue_productimage', ['product_id', 'display_order'])

        # Adding model 'ProductRecommendation'
        db.create_table(u'catalogue_productrecommendation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_recommendations', to=orm['catalogue.Product'])),
            ('recommendation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Product'])),
            ('ranking', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal(u'catalogue', ['ProductRecommendation'])

        # Adding unique constraint on 'ProductRecommendation', fields ['primary', 'recommendation']
        db.create_unique(u'catalogue_productrecommendation', ['primary_id', 'recommendation_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProductRecommendation', fields ['primary', 'recommendation']
        db.delete_unique(u'catalogue_productrecommendation', ['primary_id', 'recommendation_id'])

        # Removing unique constraint on 'ProductImage', fields ['product', 'display_order']
        db.delete_unique(u'catalogue_productimage', ['product_id', 'display_order'])

        # Removing unique constraint on 'ProductAttributeValue', fields ['attribute', 'product']
        db.delete_unique(u'catalogue_productattributevalue', ['attribute_id', 'product_id'])

        # Removing unique constraint on 'ProductCategory', fields ['product', 'category']
        db.delete_unique(u'catalogue_productcategory', ['product_id', 'category_id'])

        # Deleting model 'Category'
        db.delete_table(u'catalogue_category')

        # Deleting model 'ProductClass'
        db.delete_table(u'catalogue_productclass')

        # Removing M2M table for field options on 'ProductClass'
        db.delete_table(db.shorten_name(u'catalogue_productclass_options'))

        # Deleting model 'ProductCategory'
        db.delete_table(u'catalogue_productcategory')

        # Deleting model 'Product'
        db.delete_table(u'catalogue_product')

        # Removing M2M table for field product_options on 'Product'
        db.delete_table(db.shorten_name(u'catalogue_product_product_options'))

        # Deleting model 'ProductAttribute'
        db.delete_table(u'catalogue_productattribute')

        # Deleting model 'ProductAttributeValue'
        db.delete_table(u'catalogue_productattributevalue')

        # Deleting model 'AttributeOptionGroup'
        db.delete_table(u'catalogue_attributeoptiongroup')

        # Deleting model 'AttributeOption'
        db.delete_table(u'catalogue_attributeoption')

        # Deleting model 'AttributeEntity'
        db.delete_table(u'catalogue_attributeentity')

        # Deleting model 'AttributeEntityType'
        db.delete_table(u'catalogue_attributeentitytype')

        # Deleting model 'Option'
        db.delete_table(u'catalogue_option')

        # Deleting model 'ProductImage'
        db.delete_table(u'catalogue_productimage')

        # Deleting model 'ProductRecommendation'
        db.delete_table(u'catalogue_productrecommendation')


    models = {
        u'catalogue.attributeentity': {
            'Meta': {'object_name': 'AttributeEntity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'to': u"orm['catalogue.AttributeEntityType']"})
        },
        u'catalogue.attributeentitytype': {
            'Meta': {'object_name': 'AttributeEntityType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'catalogue.attributeoption': {
            'Meta': {'object_name': 'AttributeOption'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': u"orm['catalogue.AttributeOptionGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'catalogue.attributeoptiongroup': {
            'Meta': {'object_name': 'AttributeOptionGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'catalogue.category': {
            'Meta': {'ordering': "['full_name']", 'object_name': 'Category'},
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'catalogue.option': {
            'Meta': {'object_name': 'Option'},
            'code': ('oscar.models.fields.autoslugfield.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '128', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Required'", 'max_length': '128'})
        },
        u'catalogue.product': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Product'},
            'attributes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.ProductAttribute']", 'through': u"orm['catalogue.ProductAttributeValue']", 'symmetrical': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Category']", 'through': u"orm['catalogue.ProductCategory']", 'symmetrical': 'False'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_discountable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variants'", 'null': 'True', 'to': u"orm['catalogue.Product']"}),
            'product_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': u"orm['catalogue.ProductClass']"}),
            'product_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'recommended_products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Product']", 'symmetrical': 'False', 'through': u"orm['catalogue.ProductRecommendation']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'upc': ('oscar.models.fields.NullCharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'catalogue.productattribute': {
            'Meta': {'ordering': "['code']", 'object_name': 'ProductAttribute'},
            'code': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.AttributeEntityType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'option_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.AttributeOptionGroup']", 'null': 'True', 'blank': 'True'}),
            'product_class': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'attributes'", 'null': 'True', 'to': u"orm['catalogue.ProductClass']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '20'})
        },
        u'catalogue.productattributevalue': {
            'Meta': {'unique_together': "(('attribute', 'product'),)", 'object_name': 'ProductAttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.ProductAttribute']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attribute_values'", 'to': u"orm['catalogue.Product']"}),
            'value_boolean': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'value_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'value_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.AttributeEntity']", 'null': 'True', 'blank': 'True'}),
            'value_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'value_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'value_integer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'value_option': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.AttributeOption']", 'null': 'True', 'blank': 'True'}),
            'value_richtext': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'value_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'catalogue.productcategory': {
            'Meta': {'ordering': "['product', 'category']", 'unique_together': "(('product', 'category'),)", 'object_name': 'ProductCategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']"})
        },
        u'catalogue.productclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'ProductClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'requires_shipping': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('oscar.models.fields.autoslugfield.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '128', 'separator': "u'-'", 'blank': 'True', 'unique': 'True', 'populate_from': "'name'", 'overwrite': 'False'}),
            'track_stock': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'catalogue.productimage': {
            'Meta': {'ordering': "['display_order']", 'unique_together': "(('product', 'display_order'),)", 'object_name': 'ProductImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'display_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['catalogue.Product']"})
        },
        u'catalogue.productrecommendation': {
            'Meta': {'ordering': "['primary', '-ranking']", 'unique_together': "(('primary', 'recommendation'),)", 'object_name': 'ProductRecommendation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_recommendations'", 'to': u"orm['catalogue.Product']"}),
            'ranking': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']"})
        }
    }

    complete_apps = ['catalogue']
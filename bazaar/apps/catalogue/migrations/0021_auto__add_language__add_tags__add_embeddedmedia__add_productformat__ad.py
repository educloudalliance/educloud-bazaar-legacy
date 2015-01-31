# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table(u'catalogue_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'catalogue', ['Language'])

        # Adding M2M table for field hasLanguage on 'Language'
        m2m_table_name = db.shorten_name(u'catalogue_language_hasLanguage')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('language', models.ForeignKey(orm[u'catalogue.language'], null=False)),
            ('product', models.ForeignKey(orm[u'catalogue.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['language_id', 'product_id'])

        # Adding model 'Tags'
        db.create_table(u'catalogue_tags', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('createdAt', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastModified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['Tags'])

        # Adding M2M table for field hasTags on 'Tags'
        m2m_table_name = db.shorten_name(u'catalogue_tags_hasTags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tags', models.ForeignKey(orm[u'catalogue.tags'], null=False)),
            ('product', models.ForeignKey(orm[u'catalogue.product'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tags_id', 'product_id'])

        # Adding model 'EmbeddedMedia'
        db.create_table(u'catalogue_embeddedmedia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=4000)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Product'])),
        ))
        db.send_create_signal(u'catalogue', ['EmbeddedMedia'])

        # Adding model 'ProductFormat'
        db.create_table(u'catalogue_productformat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
        ))
        db.send_create_signal(u'catalogue', ['ProductFormat'])

        # Adding field 'Product.uuid'
        db.add_column(u'catalogue_product', 'uuid',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=50),
                      keep_default=False)

        # Adding field 'Product.materialUrl'
        db.add_column(u'catalogue_product', 'materialUrl',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Product.moreInfoUrl'
        db.add_column(u'catalogue_product', 'moreInfoUrl',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.version'
        db.add_column(u'catalogue_product', 'version',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        # Adding field 'Product.contributionDate'
        db.add_column(u'catalogue_product', 'contributionDate',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Product.maximumAge'
        db.add_column(u'catalogue_product', 'maximumAge',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Product.minimumAge'
        db.add_column(u'catalogue_product', 'minimumAge',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Product.product_format'
        db.add_column(u'catalogue_product', 'product_format',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', null=True, on_delete=models.PROTECT, to=orm['catalogue.ProductFormat']),
                      keep_default=False)

        # Adding field 'Product.contentLicense'
        db.add_column(u'catalogue_product', 'contentLicense',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4000),
                      keep_default=False)

        # Adding field 'Product.dataLicense'
        db.add_column(u'catalogue_product', 'dataLicense',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4000),
                      keep_default=False)

        # Adding field 'Product.copyrightNotice'
        db.add_column(u'catalogue_product', 'copyrightNotice',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4000),
                      keep_default=False)

        # Adding field 'Product.attributionText'
        db.add_column(u'catalogue_product', 'attributionText',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Product.attributionURL'
        db.add_column(u'catalogue_product', 'attributionURL',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4000),
                      keep_default=False)

        # Adding field 'Product.visible'
        db.add_column(u'catalogue_product', 'visible',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Product.iconUrl'
        db.add_column(u'catalogue_product', 'iconUrl',
                      self.gf('django.db.models.fields.URLField')(max_length=200, null=True),
                      keep_default=False)

        # Adding field 'Product.icon'
        db.add_column(u'catalogue_product', 'icon',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table(u'catalogue_language')

        # Removing M2M table for field hasLanguage on 'Language'
        db.delete_table(db.shorten_name(u'catalogue_language_hasLanguage'))

        # Deleting model 'Tags'
        db.delete_table(u'catalogue_tags')

        # Removing M2M table for field hasTags on 'Tags'
        db.delete_table(db.shorten_name(u'catalogue_tags_hasTags'))

        # Deleting model 'EmbeddedMedia'
        db.delete_table(u'catalogue_embeddedmedia')

        # Deleting model 'ProductFormat'
        db.delete_table(u'catalogue_productformat')

        # Deleting field 'Product.uuid'
        db.delete_column(u'catalogue_product', 'uuid')

        # Deleting field 'Product.materialUrl'
        db.delete_column(u'catalogue_product', 'materialUrl')

        # Deleting field 'Product.moreInfoUrl'
        db.delete_column(u'catalogue_product', 'moreInfoUrl')

        # Deleting field 'Product.version'
        db.delete_column(u'catalogue_product', 'version')

        # Deleting field 'Product.contributionDate'
        db.delete_column(u'catalogue_product', 'contributionDate')

        # Deleting field 'Product.maximumAge'
        db.delete_column(u'catalogue_product', 'maximumAge')

        # Deleting field 'Product.minimumAge'
        db.delete_column(u'catalogue_product', 'minimumAge')

        # Deleting field 'Product.product_format'
        db.delete_column(u'catalogue_product', 'product_format_id')

        # Deleting field 'Product.contentLicense'
        db.delete_column(u'catalogue_product', 'contentLicense')

        # Deleting field 'Product.dataLicense'
        db.delete_column(u'catalogue_product', 'dataLicense')

        # Deleting field 'Product.copyrightNotice'
        db.delete_column(u'catalogue_product', 'copyrightNotice')

        # Deleting field 'Product.attributionText'
        db.delete_column(u'catalogue_product', 'attributionText')

        # Deleting field 'Product.attributionURL'
        db.delete_column(u'catalogue_product', 'attributionURL')

        # Deleting field 'Product.visible'
        db.delete_column(u'catalogue_product', 'visible')

        # Deleting field 'Product.iconUrl'
        db.delete_column(u'catalogue_product', 'iconUrl')

        # Deleting field 'Product.icon'
        db.delete_column(u'catalogue_product', 'icon')


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
        u'catalogue.embeddedmedia': {
            'Meta': {'object_name': 'EmbeddedMedia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '4000'})
        },
        u'catalogue.language': {
            'Meta': {'object_name': 'Language'},
            'hasLanguage': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Product']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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
            'attributionText': ('django.db.models.fields.TextField', [], {}),
            'attributionURL': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Category']", 'through': u"orm['catalogue.ProductCategory']", 'symmetrical': 'False'}),
            'contentLicense': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'contributionDate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'copyrightNotice': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'dataLicense': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'iconUrl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_discountable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'materialUrl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'maximumAge': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'minimumAge': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'moreInfoUrl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'variants'", 'null': 'True', 'to': u"orm['catalogue.Product']"}),
            'product_class': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': u"orm['catalogue.ProductClass']"}),
            'product_format': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'null': 'True', 'on_delete': 'models.PROTECT', 'to': u"orm['catalogue.ProductFormat']"}),
            'product_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'recommended_products': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Product']", 'symmetrical': 'False', 'through': u"orm['catalogue.ProductRecommendation']", 'blank': 'True'}),
            'related_products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'relations'", 'blank': 'True', 'to': u"orm['catalogue.Product']"}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'upc': ('oscar.models.fields.NullCharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'Meta': {'object_name': 'ProductAttributeValue'},
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
            'Meta': {'ordering': "['product', 'category']", 'object_name': 'ProductCategory'},
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
        u'catalogue.productformat': {
            'Meta': {'object_name': 'ProductFormat'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
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
            'Meta': {'object_name': 'ProductRecommendation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_recommendations'", 'to': u"orm['catalogue.Product']"}),
            'ranking': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'recommendation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['catalogue.Product']"})
        },
        u'catalogue.tags': {
            'Meta': {'object_name': 'Tags'},
            'createdAt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hasTags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['catalogue.Product']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastModified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['catalogue']
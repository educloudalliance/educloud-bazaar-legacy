import html2text
from django import forms
from django.template.defaultfilters import slugify
from django.forms import ModelForm
from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'Product')
ProductTypes = get_model('catalogue', 'productclass')
ProductFormats = get_model('catalogue', 'ProductFormat')
ProductCategory = get_model('catalogue', 'Category')
StockRecord = get_model('partner', 'stockrecord')
Languages = get_model('catalogue', 'Language')
Tag = get_model('catalogue', 'Tags')
EmbeddedMedia = get_model('catalogue', 'EmbeddedMedia')


class EditForm(ModelForm):
    price = forms.DecimalField(min_value=0, max_value=9999, max_digits=2, required=True)
    embedMedia = forms.CharField(label='Embedded media', required=False, help_text='Please Use comma (,) to separate links (eg. http://www.test.test/media,http://www.test.test/medi2,http://www.test.test/media3)') # TODO Better
    tags = forms.CharField(label='Tags', required=False, help_text='Please Use comma (,) to separate tags (eg. math,awesome,game)') # TODO Better
    subjects = forms.ModelMultipleChoiceField(label='Subjects', queryset=ProductCategory.objects.all(), required=True)
    language = forms.ModelMultipleChoiceField(label='Languages', queryset=Languages.objects.all())

    '''
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = ProductCategory.objects.filter(product=Product)
    '''
    class Meta:
        model = Product
        fields = ['title', 'description', 'materialUrl', 'iconUrl', 'product_format', 'product_class', 'moreInfoUrl', 'version', 'visible', 'contributionDate', 'maximumAge', 'minimumAge', 'contentLicense', 'dataLicense', 'copyrightNotice', 'attributionText', 'attributionURL']

    def save(self, commit=True):
        super(EditForm, self).save(commit=commit)

    def clean_description(self):
        data = self.cleaned_data['description']
        data = html2text.html2text(data)
        return data

    def clean(self):
        cleaned_data = super(EditForm, self).clean()
        tags = cleaned_data.get("tags")

        tagsList = tags.split(',')

        # Check if there's too many tags
        if len(tagsList) > 10:
            raise forms.ValidationError('Too many tags (Max. 10)')

        return self.cleaned_data



class NewForm(ModelForm):
    uuid = forms.CharField(label='UUID', required=True)
    price = forms.DecimalField(min_value=0, max_value=9999, max_digits=2, required=True)
    embedMedia = forms.CharField(label='Embedded media', required=False, help_text='Please Use comma (,) to separate links (eg. http://www.test.test/media,http://www.test.test/medi2,http://www.test.test/media3)') # TODO Better
    tags = forms.CharField(label='Tags', required=False, help_text='Please Use comma (,) to separate tags (eg. math,awesome,game)') # TODO Better
    subjects = forms.ModelMultipleChoiceField(label='Subjects', queryset=ProductCategory.objects.all(), required=True)
    language = forms.ModelMultipleChoiceField(label='Languages', queryset=Languages.objects.all())

    '''
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = ProductCategory.objects.filter(product=Product)
    '''
    class Meta:
        model = Product
        fields = ['uuid', 'title', 'description', 'materialUrl', 'iconUrl', 'product_format', 'product_class', 'moreInfoUrl', 'version', 'visible', 'contributionDate', 'maximumAge', 'minimumAge', 'contentLicense', 'dataLicense', 'copyrightNotice', 'attributionText', 'attributionURL']

    def save(self, commit=True):
        super(NewForm, self).save(commit=commit)

    def clean_description(self):
        data = self.cleaned_data['description']
        data = html2text.html2text(data)
        return data


    def clean(self):
        cleaned_data = super(NewForm, self).clean()
        uuid = cleaned_data.get("uuid")
        tags = cleaned_data.get("tags")

        tagsList = tags.split(',')

        # Check if there's too many tags
        if len(tagsList) > 10:
            raise forms.ValidationError('Too many tags (Max. 10)')

        # Check if uuid is already used
        uuid = slugify(uuid)
        if StockRecord.objects.filter(partner_sku=uuid).exists():
            raise forms.ValidationError('UUID already in use')

        return self.cleaned_data

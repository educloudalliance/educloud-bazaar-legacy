from django import forms
from django.forms import ModelForm
from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'Product')
ProductTypes = get_model('catalogue', 'productclass')
ProductFormats = get_model('catalogue', 'ProductFormat')
ProductCategory = get_model('catalogue', 'Category')
Languages = get_model('catalogue', 'Language')


class EditForm(ModelForm):
    embedMedia = forms.CharField(label='Embedded media', required=False) # TODO Better
    tags = forms.CharField(label='Tags', required=False) # TODO Better
    subjects = forms.ModelMultipleChoiceField(label='Subjects', queryset=ProductCategory.objects.all(), required=True)
    language = forms.ModelMultipleChoiceField(label='Languages', queryset=Languages.objects.all())

    '''
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = ProductCategory.objects.filter(product=Product)
    '''
    class Meta:
        model = Product
        fields = ['title', 'description', 'materialUrl', 'iconUrl', 'product_format', 'product_class', 'moreInfoUrl', 'version', 'visible', 'contributionDate', 'maximumAge', 'minimumAge', 'contentLicense', 'dataLicense', 'copyrightNotice']

    def save(self, commit=True):
        super(EditForm, self).save(commit=commit)


class NewForm(ModelForm):
    uuid = forms.CharField(label='UUID', required=True)
    price = forms.DecimalField(min_value=0, max_value=9999, max_digits=2, required=True)
    embedMedia = forms.CharField(label='Embedded media', required=False) # TODO Better
    tags = forms.CharField(label='Tags', required=False) # TODO Better
    subjects = forms.ModelMultipleChoiceField(label='Subjects', queryset=ProductCategory.objects.all(), required=True)
    language = forms.ModelMultipleChoiceField(label='Languages', queryset=Languages.objects.all())

    '''
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = ProductCategory.objects.filter(product=Product)
    '''
    class Meta:
        model = Product
        fields = ['uuid', 'title', 'description', 'materialUrl', 'iconUrl', 'product_format', 'product_class', 'moreInfoUrl', 'version', 'visible', 'contributionDate', 'maximumAge', 'minimumAge', 'contentLicense', 'dataLicense', 'copyrightNotice']

    def save(self, commit=True):
        super(NewForm, self).save(commit=commit)
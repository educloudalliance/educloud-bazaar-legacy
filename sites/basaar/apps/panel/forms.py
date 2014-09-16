from django import forms
from django.forms import ModelForm
from oscar.core.loading import get_class, get_model

Product = get_model('catalogue', 'Product')
ProductTypes = get_model('catalogue', 'productclass')
ProductFormats = get_model('catalogue', 'ProductFormat')
ProductCategory = get_model('catalogue', 'ProductCategory')
Languages = get_model('catalogue', 'Language')


class EditForm(ModelForm):
    embedMedia = forms.CharField(label='Embedded media') # TODO Better
    tags = forms.CharField(label='Tags') # TODO Better
    subjects = forms.ModelMultipleChoiceField(label='Subjects', queryset=ProductCategory.objects.all(), required=True)
    language = forms.ModelMultipleChoiceField(label='Languages', queryset=Languages.objects.all())

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = ProductCategory.object.filter(product=Product)

    class Meta:
        model = Product
        fields = ['title', 'description', 'materialUrl', 'iconUrl', 'product_format', 'product_class', 'moreInfoUrl', 'version', 'visible', 'contributionDate', 'maximumAge', 'minimumAge', 'contentLicense', 'dataLicense', 'copyrightNotice']

    def save(self, commit=True):

        super(EditForm, self).save(commit=commit)

class NewForm(ModelForm):
    model = Product
    fields = ['pub_date', 'headline', 'content', 'reporter']

'''
class NewForm(forms.Form):
    uuid = forms.CharField(label='Uuid', max_length=100)
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', widget=forms.Textarea)
    materialUrl = forms.URLField(label='Material URL', max_length=256)
    productType = forms.ModelChoiceField(label='Product type', queryset=ProductTypes.objects.all())
    productFormat = forms.ModelChoiceField(label='Product format', queryset=ProductFormats.objects.all())
    iconUrl = forms.URLField(label='Icon URL', max_length=256)
    embedMedia = forms.CharField(label='Embedded media') # TODO Better
    moreInfoUrl = forms.URLField(label='More info URL', max_length=256)
    version = forms.CharField(label='Version', max_length=10)
    price = forms.DecimalField(label='Price', max_value=99999, min_value=0)
    tags = forms.CharField(label='Tags') # TODO Better
    visible = forms.BooleanField(label='Visibility')
    subjects = forms.ModelMultipleChoiceField(label='Subjects', queryset=Subjects.objects.all())
    language = forms.ModelMultipleChoiceField(label='Languages', queryset=Languages.objects.all())
    contributionDate = forms.DateField(label='Contribution Date', input_formats=['%Y-%m-%d'])
    maximumAge = forms.DecimalField(label='Maximum age', max_value=99, min_value=0, decimal_places=0)
    minimumAge = forms.DecimalField(label='Minimum age', max_value=99, min_value=0, decimal_places=0)
    contentLicense = forms.CharField(label='Content License')
    dataLicense = forms.CharField(label='Data License')
    copyrightNotice = forms.CharField(label='Copyright Notice')
    attributionText = forms.CharField(label='Attribution Text')
    attributionURL = forms.URLField(label='Attribution URL', max_length=256)
'''
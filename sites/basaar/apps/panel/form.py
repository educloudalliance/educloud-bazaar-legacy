from django import forms

class EditForm(forms.form):
    title = form.CharField(label='Title', max_lenght=100)

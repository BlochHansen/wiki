from django import forms

class entryForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    text = forms.CharField(widget=forms.Textarea)


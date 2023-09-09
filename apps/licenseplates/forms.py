from django import forms


class LicensePlateForm(forms.Form):
    number = forms.CharField(label='Number', max_length=100)

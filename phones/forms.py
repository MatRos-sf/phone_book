from .models import Person, Phone, Mail
from django import forms

class PersonForms(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           "placeholder": "Name"}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                           "placeholder": "Phone"}))
    class Meta:
        model = Person
        fields = ('name', 'surname', )

class PhoneForms(forms.ModelForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control',
                                                           "placeholder": "Phone"}))
    class Meta:
        model = Phone
        fields = ('phone',)

class MailForms(forms.ModelForm):
    mail = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           "placeholder": "Mail"}))
    class Meta:
        model = Mail
        fields = ('mail',)

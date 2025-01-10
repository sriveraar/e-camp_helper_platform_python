from django import forms
from .models import Provider

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'contact_info', 'service', 'profile_picture']

from django import forms
from django.contrib.auth.models import User
from .models import Provider, ProviderProfile, Service

class ProviderForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Provider
        fields = ['email', 'atencion', 'telefono', 'nombres', 'apellidos', 'descripcion', 'foto']

    def save(self, commit=True):
        provider = super().save(commit=False)
        if commit:
            user = User.objects.create_user(username=self.cleaned_data['email'], password=self.cleaned_data['password'])
            provider.user = user
            provider.save()
        return provider

class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ['services']  # Los servicios que el proveedor ofrece

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Para mostrar como casillas de verificación
        required=False
    )
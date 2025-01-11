from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Provider

class ProviderForm(UserCreationForm):
    email = forms.EmailField()
    atencion = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    descripcion = forms.CharField(widget=forms.Textarea)
    foto = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Crear el perfil del proveedor
            provider = Provider(
                user=user,
                email=self.cleaned_data['email'],
                atencion=self.cleaned_data['atencion'],
                telefono=self.cleaned_data['telefono'],
                nombres=self.cleaned_data['nombres'],
                apellidos=self.cleaned_data['apellidos'],
                descripcion=self.cleaned_data['descripcion'],
                foto=self.cleaned_data['foto']
            )
            provider.save()
        return user

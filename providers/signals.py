from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProviderProfile

@receiver(post_save, sender=User)
def create_provider_profile(sender, instance, created, **kwargs):
    """Crea un perfil de proveedor cuando un nuevo usuario se registre."""
    if created:
        # Solo crear el perfil de proveedor si el usuario es nuevo
        ProviderProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_provider_profile(sender, instance, **kwargs):
    """Guarda el perfil de proveedor cuando se guarda el usuario."""
    try:
        instance.provider_profile.save()
    except ProviderProfile.DoesNotExist:
        # Si no existe el perfil de proveedor, lo crea
        ProviderProfile.objects.create(user=instance)

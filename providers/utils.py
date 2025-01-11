from .models import ProviderProfile

def create_provider_profile(user):
    """
    Crea el perfil del proveedor si no existe.
    """
    if not hasattr(user, 'provider_profile'):
        # Crear el perfil si no existe
        provider_profile = ProviderProfile.objects.create(user=user)
        return provider_profile
    return None

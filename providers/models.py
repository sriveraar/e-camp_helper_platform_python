from django.contrib.auth.models import User
from django.db import models

# Modelo para los Servicios
class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Modelo para los Proveedores
class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    atencion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='provider_photos/', null=True, blank=True)
    services = models.ManyToManyField(Service, through='ProviderService')

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"



# Tabla intermedia para la relación muchos a muchos entre Proveedor y Servicio
class ProviderService(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.provider} - {self.service}"


# Modelo para los Mensajes de los Proveedores
class Message(models.Model):
    provider = models.ForeignKey(Provider, related_name='messages', on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=255)
    sender_email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message to {self.provider.email} from {self.sender_name}"


# Modelo de perfil de proveedor (con relación a User)
class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

def create_provider_profile(user):
    if not hasattr(user, 'provider_profile'):
        ProviderProfile.objects.create(user=user)
        
    def __str__(self):
        return f"Perfil de {self.user.username}"
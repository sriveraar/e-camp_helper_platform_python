from django.contrib.auth.models import User
from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    atencion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='provider_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Message(models.Model):
    provider = models.ForeignKey(Provider, related_name='messages', on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=255)
    sender_email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message to {self.provider.user.email} from {self.sender_name}"

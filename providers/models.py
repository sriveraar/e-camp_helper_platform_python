from django.contrib.auth.models import User
from django.db import models

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    availability_hours = models.CharField(max_length=255, help_text="Formato: Lunes a Viernes, 9:00 AM - 6:00 PM")
    phone = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

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

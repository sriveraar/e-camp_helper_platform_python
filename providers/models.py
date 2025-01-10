from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()
    service = models.ForeignKey(Service, related_name='providers', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

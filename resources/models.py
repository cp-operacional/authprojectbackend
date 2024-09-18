from django.db import models
from django.conf import settings

class Resource(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    year = models.IntegerField()
    pantone_value = models.CharField(max_length=20)

    def __str__(self):
        return self.name

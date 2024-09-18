from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    year = models.IntegerField()
    pantone_value = models.CharField(max_length=20)

    def __str__(self):
        return self.name

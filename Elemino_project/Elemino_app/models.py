from django.db import models


class Performance(models.Model):
    pet_id = models.IntegerField(unique=True)
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    date_registered = models.DateField()

    class Meta:
        ordering = ['pet_name']

    def __str__(self):
        return f"{self.pet_name} ({self.pet_id})"
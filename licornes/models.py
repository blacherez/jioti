from django.db import models

# Create your models here.

class Licorne(models.Model):
    nom = models.CharField(max_length=200)
    creation_date = models.DateField('Date de création')
    photo = models.CharField(max_length=200)
    identifiant = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Etape(models.Model):
    licorne = models.ForeignKey(Licorne, on_delete=models.CASCADE)
    etape_date = models.DateField()
    localisation = models.CharField(max_length=100)
    current = models.BooleanField()

    def __str__(self):
        return ("Etape de %s (%s)" % (self.licorne.nom, self.etape_date))
